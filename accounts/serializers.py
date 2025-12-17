from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer for User Data (Profile)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Serializer for Registration (The Critical Part)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']
        # Note: If your User model doesn't have phone_number, remove it from fields above

    def create(self, validated_data):
        # This handles the phone_number field if it's passed but not in the default User model
        phone = validated_data.pop('phone_number', '')
       
        # CRITICAL FIX: We use 'create_user' to properly encrypt the password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user