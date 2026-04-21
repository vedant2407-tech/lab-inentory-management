from django.urls import path

from .views import (
    AddItem,
    DeleteItem,
    InventoryDashboard,
    UpdateItem,
    export_items_csv,
    issue_item,
    return_item,
)

urlpatterns = [
    path("dashboard/", InventoryDashboard.as_view(), name="dashboard"),
    path("items/add/", AddItem.as_view(), name="add-item"),
    path("items/<int:pk>/edit/", UpdateItem.as_view(), name="update-item"),
    path("items/<int:pk>/delete/", DeleteItem.as_view(), name="delete-item"),
    path("items/<int:pk>/issue/", issue_item, name="issue-item"),
    path("issues/<int:issue_id>/return/", return_item, name="return-item"),
    path("items/export/csv/", export_items_csv, name="export-csv"),
]
