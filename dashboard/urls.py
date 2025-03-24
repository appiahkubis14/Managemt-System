from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from inventory.views import *
from transport.views import *
from warehouse.views import *
from ampPortal.views import *
from employees.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("dashboard/home/", dashboard_view, name="dashboard_home"),
    path("dashboard/transport/", transport_view, name="dashboard_transport"),
    path("dashboard/inventory/", inventory_view, name="dashboard_inventory"),
    path("dashboard/warehouse/", warehouse_view, name="dashboard_warehouse"),
    path("dashboard/tracking/", tracking_view, name="dashboard_tracking"),
    path('dashboard/employees/', employee_list, name='employee_list'),

]



