from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 1. The new Home path
    path('', views.home, name='home'),

    # 2. Admin path
    path('admin/', admin.site.urls),

    path('api/services/', include('services.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/transaction/', include('transaction.urls')),
]