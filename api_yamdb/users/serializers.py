"""Serializers for users app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from .validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

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
            user_instance, created = User.objects.get_or_create(
                **validated_data)
            return user_instance
        except IntegrityError as e:
            raise ValidationError(e)


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer for ConfirmationCode model."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        """Validate serializer's data."""
        user = get_object_or_404(User, username=data.get('username', ''))
        data['user'] = user
        confirmation_code = data.get('confirmation_code', '')
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError(
                'Отсутствует обязательное поле или оно некорректно')
        return super().validate(data)
