from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Team

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "profile_picture", "bio", "phone_number", "team", "email_notifications", "push_notifications"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_role(self, value):
        if value not in ["admin", "partial_admin", "user"]:
            raise serializers.ValidationError("Invalid role selection.")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
