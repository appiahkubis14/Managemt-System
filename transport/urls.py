from .views import *
from django.urls import path

urlpatterns = [
    path("transport-dashboard/", transport_view, name="transport_dashboard"),
    path("vehicle-list",vehicle_view,name='vehicle_view')
]