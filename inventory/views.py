import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.decorators.http import require_POST

from .models import ItemIssue, LabItem


class InventoryDashboard(LoginRequiredMixin, ListView):
    model = LabItem
    template_name = "inventory/dashboard.html"
    context_object_name = "items"

    def get_queryset(self):
        return LabItem.objects.filter(owner=self.request.user).order_by("-date_added")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']
        context['total_items'] = items.count()
        context['low_stock_items'] = items.filter(quantity__lt=5).count()
        # counts by status
        context['status_counts'] = {
            'in_stock': items.filter(status=LabItem._meta.get_field('status').choices[0][0]).count(),
            'out_of_stock': items.filter(status=LabItem._meta.get_field('status').choices[1][0]).count(),
            'damaged': items.filter(status=LabItem._meta.get_field('status').choices[2][0]).count(),
        }
        context['recent_issues'] = ItemIssue.objects.filter(item__owner=self.request.user).select_related('item')[:20]
        return context


class AddItem(LoginRequiredMixin, CreateView):
    model = LabItem
    fields = ["name", "quantity", "category", "status"]
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = LabItem
    fields = ["name", "quantity", "category", "status"]
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return LabItem.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        # ensure we're updating the existing object (protect against accidental CREATE)
        obj = self.get_object()
        form.instance.pk = obj.pk
        form.instance.owner = self.request.user
        return super().form_valid(form)


def export_items_csv(request):
    from django.http import HttpResponse

    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    items = LabItem.objects.filter(owner=request.user).order_by('name')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lab_items.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Quantity', 'Status', 'Location', 'Date Added'])
    for it in items:
        writer.writerow([it.name, it.category, it.quantity, it.status, getattr(it, 'location', ''), it.date_added])

    return response


@login_required
@require_POST
def issue_item(request, pk):
    item = get_object_or_404(LabItem, pk=pk, owner=request.user)
    student_name = request.POST.get('student_name', '').strip()

    if not student_name:
        messages.error(request, 'Student name is required to issue a component.')
        return redirect('dashboard')

    if item.quantity <= 0:
        messages.error(request, f'{item.name} is out of stock.')
        return redirect('dashboard')

    if item.issues.filter(returned_at__isnull=True).exists():
        messages.error(request, f'{item.name} is already issued and not yet returned.')
        return redirect('dashboard')

    ItemIssue.objects.create(item=item, student_name=student_name)
    item.quantity -= 1
    if item.quantity == 0:
        item.status = 'out_of_stock'
    item.save(update_fields=['quantity', 'status'])

    messages.success(request, f'{item.name} issued to {student_name}.')
    return redirect('dashboard')


@login_required
@require_POST
def return_item(request, issue_id):
    issue = get_object_or_404(ItemIssue, pk=issue_id, item__owner=request.user)

    if issue.returned_at is not None:
        messages.info(request, 'This issue entry is already marked as returned.')
        return redirect('dashboard')

    issue.returned_at = timezone.now()
    issue.save(update_fields=['returned_at'])

    item = issue.item
    item.quantity += 1
    if item.status == 'out_of_stock':
        item.status = 'in_stock'
    item.save(update_fields=['quantity', 'status'])

    messages.success(request, f'{item.name} returned by {issue.student_name}.')
    return redirect('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = LabItem
    template_name = "inventory/item_confirm_delete.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return LabItem.objects.filter(owner=self.request.user)
