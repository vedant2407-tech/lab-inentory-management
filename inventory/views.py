from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import LabItem


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
    import csv

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


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = LabItem
    template_name = "inventory/item_confirm_delete.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return LabItem.objects.filter(owner=self.request.user)
