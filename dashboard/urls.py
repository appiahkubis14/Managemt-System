from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from inventory.views import *
from transport.views import *
from warehouse.views import *
from ampPortal.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("dashboard/home/", dashboard_view, name="dashboard_home"),
    path("dashboard/transport/", transport_view, name="dashboard_transport"),
    path("dashboard/inventory/", inventory_view, name="dashboard_inventory"),
    path("dashboard/warehouse/", warehouse_view, name="dashboard_warehouse"),
    path("dashboard/tracking/", tracking_view, name="dashboard_tracking"),


    #Transport
    path("transport/vehicles/", vehicle_view, name='dashboard_transport_vehicles'),  # Render vehicle template
    path("transport/vehicles/", vehicle_list, name='transport_vehicle_list'),  # List all vehicles
    path("transport/vehicles/create/", vehicle_create, name='transport_vehicle_create'),  # Create a vehicle
    path("transport/vehicles/<str:vehicle_id>/", vehicle_detail, name='transport_vehicle_detail'),  # Retrieve vehicle
    path("transport/vehicles/<str:vehicle_id>/update/", vehicle_update, name='transport_vehicle_update'),  # Update vehicle
    path("transport/vehicles/<str:vehicle_id>/delete/", vehicle_delete, name='transport_vehicle_delete'),  # Delete vehicle
]



