from .views import *
from django.urls import path

urlpatterns = [
    path("warehouse-dashboard/", warehouse_view, name="warehouse_dashboard"),
    
]