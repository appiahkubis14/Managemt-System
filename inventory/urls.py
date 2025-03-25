from .views import *
from django.urls import path

urlpatterns = [
    path("inventory-dashboard/", inventory_view, name="inventory_dashboard"),
    # path("add-item/", add_item, name="add_item"),
    path("view-inventories/", inventory_view, name="view_inventories"),
    # path("update-item/<str:id>/", update_item, name="update_item"),
    # path("delete-item/<str:id>/", delete_item, name="delete_item"),
    # path("export/", export_inventory_csv, name="export_inventory_csv"),
    # path("import/", import_inventory, name="import_inventory"),
    
]