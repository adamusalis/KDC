from rest_framework import serializers

class PurchaseSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)
    # We don't need the user ID because we get that from the Token automatically