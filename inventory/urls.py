from .views import *
from django.urls import path

urlpatterns = [
    # path("dashboard/", inventory_dashboard_view, name="inventory_dashboard"),
    path("view-inventories/", inventory_view, name="view_inventories"),
    path("requested-inventory/", requested_inventory , name="inventory-request") ,
    path("all-request-inventory/", get_inventory_requests , name="request-inventory") ,
    path('create/', create_inventory, name='create_inventory'),
    path('update/<int:id>/', update_inventory, name='update_inventory'),
    path('delete/<int:id>/', delete_inventory, name='delete_inventory'),

    path("request-inventory/update/<str:id>/", update_transaction_type,name='update_inventory_request'),
    path("inventory-request/<int:id>/<str:action>/", process_request, name="process_request"),



    path('inventory-items/', inventory_items, name='inventory_items'),
    path('process-request/<int:id>/<str:action>/', process_request, name='process_request'),

    path('api/request-inventory/', add_inventory_request, name='add-inventory-request'),
    path('update-request-inventory/', update_inventory_request, name='update-inventory-request'),
    path('delete-request-inventory/', delete_inventory_request, name='delete-inventory-request'),

    path("bulk/",BulkInventoryCreateView.as_view(),name='bulk')
]
    
