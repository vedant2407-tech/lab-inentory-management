from django.contrib import admin

from .models import LabItem


@admin.register(LabItem)
class LabItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "owner", "date_added")
    list_filter = ("category", "owner")
    search_fields = ("name", "category")
