"""Serializers for users app."""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .constants import NOT_ALLOWED_NAMES_FOR_USERS

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    user_types = ('user', 'moderator', 'admin',)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=1000000, required=False)
    role = serializers.ChoiceField(choices=user_types, required=False)

    class Meta:
        """Meta-data of UserSerialzier class."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class SignupSerializer(serializers.ModelSerializer):
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
