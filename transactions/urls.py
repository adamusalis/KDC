from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_data, name='purchase_data'),
    path('fund/', views.fund_wallet, name='fund_wallet'), # <--- Add this line
]