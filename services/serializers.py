from rest_framework import serializers
from .models import Network, DataPlan

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['id', 'name', 'status']

class DataPlanSerializer(serializers.ModelSerializer):
    # We want to show the Network name instead of just the ID number
    network_name = serializers.CharField(source='network.name', read_only=True)

    class Meta:
        model = DataPlan
        fields = ['id', 'network', 'network_name', 'plan_type', 'name', 'price', 'plan_id']