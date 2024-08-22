from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','user_type','is_active','is_staff','is_superuser', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()  # Use a single token field for Django Token Authentication

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('username','user_type','is_active')
        # fields = "__all__"  # Or use "__all__" if you want to expose all fields
