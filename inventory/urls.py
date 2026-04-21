from django.urls import path

from .views import AddItem, DeleteItem, InventoryDashboard, UpdateItem, export_items_csv

urlpatterns = [
    path("dashboard/", InventoryDashboard.as_view(), name="dashboard"),
    path("items/add/", AddItem.as_view(), name="add-item"),
    path("items/<int:pk>/edit/", UpdateItem.as_view(), name="update-item"),
    path("items/<int:pk>/delete/", DeleteItem.as_view(), name="delete-item"),
    path("items/export/csv/", export_items_csv, name="export-csv"),
]
