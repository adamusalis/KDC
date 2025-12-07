from django.urls import path
from . import views

urlpatterns = [
    path('networks/', views.get_networks, name='get_networks'),
    path('plans/', views.get_plans, name='get_plans'),
]