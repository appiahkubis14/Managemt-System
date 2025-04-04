from .views import *
from django.urls import path

urlpatterns = [
    path("transport-dashboard/", transport_view, name="transport_dashboard"),
    
    path('data/', transport_data, name='transport_data'),
    # path("vehicle-list",vehicle_view,name='vehicle_view'),
    path('export/', export_vehicles_csv, name='export_vehicles'),
    path('import/', import_vehicles, name='import_vehicles'),

    #NEW API WORKING
    path('dashboard/', vehicle_view, name='dashboard'),  # Your dashboard view
    path('api/vehicles/', vehicle_list_api, name='vehicle_list_api'),  #
    path('vehicles/add/', add_vehicle, name='add_vehicle'),  # POST to add a vehicle
    path('vehicles/<int:vehicle_id>/', get_vehicles, name='get_vehicle_details'),  # GET single vehicle
    path('vehicles/<int:vehicle_id>/update/', update_vehicle, name='update_vehicle'),  # PUT to update vehicle
    path('vehicles/<int:vehicle_id>/delete/', delete_vehicle, name='delete_vehicle'),  # DELETE vehicle
    

    path("driver_assistant_assignment/", driver_assistant_assignment_page, name="driver_assistant_assignment_page"),
    path("api/assignments/", get_assignments, name="get_assignments"),
    path("api/assignments/create/", create_assignment, name="add_assignment"),
    path("api/assignments/<int:assignment_id>/update/", update_assignment, name="update_assignment"),
    path("api/assignments/<int:assignment_id>/delete/", delete_assignment, name="delete_assignment"),
    # path("api/assignments/import/", import_assignments, name="import_assignments"),
    # path("api/assignments/export/", export_assignments, name="export_assignments"),
    
    path("vehicles/", vehicle_view, name='dashboard_vehicles'),  # Render vehicle template
    path("vehicles/list/", vehicle_list, name='vehicle_list'),  # List all vehicles
    path("vehicles/create/", vehicle_create, name='vehicle_create'),  # Create a vehicle
    path("vehicles/<int:id>/", vehicle_detail, name='vehicle_detail'),  # Retrieve vehicle
    path("vehicles/<int:id>/update/", vehicle_update, name='vehicle_update'),  # Update vehicle
    path("vehicles/<int:id>/delete/", vehicle_delete, name='vehicle_delete'),  # Delete vehicle
    
    # path("driver_assistant_assignment/", driver_assistant_assignment, name='driver_assistant_assignment'),  # Render driver template
    path("delivery_schedule/", delivery_schedule, name='delivery_schedule'),  # Render driver template
    path("maintenance-request/" , maintenance_request,name="maintenance_request"),
    path("transport-requested-inventory/", requested_inventory , name="inventory-request") ,


    path("get-maintenance-requests/", get_maintenance_requests, name="get_maintenance_requests"),
    path("create-maintenance-request/", create_maintenance_request, name="create_maintenance_request"),
    path("create-new-maintenance-request/", create_new_maintenance_request, name="create_maintenance_request"),
    path("update-maintenance-request/<int:request_id>/", update_maintenance_request, name="update_maintenance_request"),
    path("delete-maintenance-request/<int:request_id>/", delete_maintenance_request, name="delete_maintenance_request"),
    # path('client-request/create/', create_client_request, name='create_client_request'),

    path("assignments/create/", create_vehicle_assignment, name="create_vehicle_assignment"),
    path("assignments/update/<int:pk>/", update_vehicle_assignment, name="update_vehicle_assignment"),
    path("assignments/delete/<int:pk>/", delete_vehicle_assignment, name="delete_vehicle_assignment"),

    #  path('get-vehicle-assignment/<int:vehicle_id>/', get_vehicle_assignment, name='get_vehicle_assignment'),
    path('client-requests/', client_requests_list, name='client_requests_list'),
    path('client-requests-list/', fetch_client_requests, name="fetch_client_requests"),
    path('create_client_request/', create_client_request, name="create_client_request"),
    path('client-requests/edit/<int:request_id>/', update_client_request, name="update_client_request"),
    path('client-requests/delete/<int:request_id>/', delete_client_request, name="delete_client_request"),
    path("client-request/details/<int:request_id>/", get_client_request_details, name="client_request_details"),


    #  path("transport/dispatches/", get_dispatches, name="get_dispatches"),
    path('dispatches/', dispatch_list, name='dispatch-list'),
    path("dispatch/create/", create_dispatch_request, name="create_dispatch"),
    path("dispatch/update/<int:dispatch_id>/", update_dispatch_request, name="update_dispatch"),
    path("dispatch/delete/<int:dispatch_id>/", delete_dispatch_request, name="delete_dispatch"),



    path('inventory/view/', inventory_view, name='inventory_view'),
    path('inventory/requested/', requested_inventory, name='requested_inventory'),
    path('api/get-maintenance/<int:maintenance_id>/', get_maintenance_request_details, name='get_maintenance_details'),
    
    path('inventory-requests/', get_inventory_requests, name='get_inventory_requests'),
    path('inventory-requests/<int:id>/', get_inventory_request_detail, name='get_inventory_request_detail'),
    
    path('inventory-request/add/', add_inventory_request, name='add_inventory_request'),
    path('inventory-request/update/', update_inventory_request, name='update_inventory_request'),
    path('inventory-request/delete/', delete_inventory_request, name='delete_inventory_request'),

]



