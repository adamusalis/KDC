from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    # EXPLICITLY DEFINE phone_number so it doesn't crash the default User model
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        # We include 'phone_number' here now that it is defined above
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']

    def create(self, validated_data):
        # Remove phone_number before creating the user (since User model doesn't have it)
        phone = validated_data.pop('phone_number', '')
       
        # Create the user safely
        # Create the user safely
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user