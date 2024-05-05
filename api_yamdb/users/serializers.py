"""Serializers for users app."""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .constants import NOT_ALLOWED_NAMES_FOR_USERS

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Base serializer for User model."""

    email = serializers.EmailField(max_length=254, required=True)

    def validate_email(self, value):
        """Validate field email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value


class UserSerializer(BaseUserSerializer):
    """Serializer for User model."""

    class Meta:
        """Meta-data of UserSerialzier class."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class SignupSerializer(BaseUserSerializer):
    """Serializer for SignupAPIView to work with User model."""

    class Meta:
        """Meta-data of SignupSerialzier class."""

        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        """Validate field username."""
        if value in NOT_ALLOWED_NAMES_FOR_USERS:
            raise serializers.ValidationError(
                'Нельзя использовать это имя')
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer for ConfirmationCode model."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.IntegerField()
