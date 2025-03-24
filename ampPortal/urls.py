from django.urls import path
from .views import tracking_view


urlpatterns = [
    path('tracking-dashboard/', tracking_view, name='tracking_dashboard'),
]
