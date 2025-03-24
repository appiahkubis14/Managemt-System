from .views import *
from django.urls import path

urlpatterns = [
    path("inventory-dashboard/", inventory_view, name="inventory_dashboard"),
    
]