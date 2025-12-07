from django.contrib import admin

from django.contrib import admin
from .models import Network, DataPlan

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

@admin.register(DataPlan)
class DataPlanAdmin(admin.ModelAdmin):
    list_display = ('network', 'plan_type', 'name', 'price', 'plan_id')
    list_filter = ('network', 'plan_type') # Adds a sidebar filter