from django.contrib import admin

from .models import ItemIssue, LabItem


@admin.register(LabItem)
class LabItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "owner", "date_added")
    list_filter = ("category", "owner")
    search_fields = ("name", "category")


@admin.register(ItemIssue)
class ItemIssueAdmin(admin.ModelAdmin):
    list_display = ("item", "student_name", "taken_at", "returned_at")
    list_filter = ("taken_at", "returned_at")
    search_fields = ("item__name", "student_name")
