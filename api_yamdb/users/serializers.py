"""Serializers for users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from .constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from .validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH, required=True,
        validators=(UniqueValidator(User.objects.all(),
                                    'This email already exists.'),)
    )

    class Meta:
        """Meta-data of UserSerialzier class."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class SignupSerializer(serializers.Serializer):
    """Serializer for SignupAPIView to work with User model."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=(UnicodeUsernameValidator(), validate_username,))
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)

    def create(self, validated_data):
        """Execute when POST method."""
        try:
            return User.objects.get(**validated_data)
        except User.DoesNotExist:
            try:
                return User.objects.create(**validated_data)
            except IntegrityError as e:
                raise ValidationError(e)


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer for ConfirmationCode model."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
