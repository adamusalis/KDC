from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Network, DataPlan
from .serializers import NetworkSerializer, DataPlanSerializer

@api_view(['GET'])
@permission_classes([AllowAny]) # Allow anyone to see products (even if not logged in)
def get_networks(request):
    networks = Network.objects.filter(status=True) # Only show active networks
    serializer = NetworkSerializer(networks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_plans(request):
    # We can filter by network if provided in the URL (e.g., ?network_id=1)
    network_id = request.query_params.get('network_id')
   
    if network_id:
        plans = DataPlan.objects.filter(network_id=network_id)
    else:
        plans = DataPlan.objects.all()
       
    serializer = DataPlanSerializer(plans, many=True)
    return Response(serializer.data)