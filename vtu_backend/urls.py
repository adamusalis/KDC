from django.contrib import admin
from django.urls import path, include  # <--- Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/services/', include('services.urls')), # <--- Add this line
    path('api/auth/', include('accounts.urls')),
    path('api/transaction/', include('transactions.urls')),
]