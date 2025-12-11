from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 1. The Home Path (Simple and clean)
    path('', views.home, name='home'),

    # 2. Admin Path
    path('admin/', admin.site.urls),

    # 3. Your API Paths
    path('api/services/', include('services.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/transaction/', include('transaction.urls')),
]