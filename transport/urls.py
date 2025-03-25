from .views import *
from django.urls import path

urlpatterns = [
    path("transport-dashboard/", transport_view, name="transport_dashboard"),
    path("vehicle-list",vehicle_view,name='vehicle_view'),
    path('export/', export_vehicles_csv, name='export_vehicles'),
    path('import/', import_vehicles, name='import_vehicles'),
    
    path("vehicles/", vehicle_view, name='dashboard_vehicles'),  # Render vehicle template
    path("vehicles/list/", vehicle_list, name='vehicle_list'),  # List all vehicles
    path("vehicles/create/", vehicle_create, name='vehicle_create'),  # Create a vehicle
    path("vehicles/<int:id>/", vehicle_detail, name='vehicle_detail'),  # Retrieve vehicle
    path("vehicles/<int:id>/update/", vehicle_update, name='vehicle_update'),  # Update vehicle
    path("vehicles/<int:id>/delete/", vehicle_delete, name='vehicle_delete'),  # Delete vehicle
    
    path("driver_assistant_assignment/", driver_assistant_assignment, name='driver_assistant_assignment'),  # Render driver template
]



