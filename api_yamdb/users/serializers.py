"""Serializers for users app."""
from rest_framework import serializers
from django.contrib.auth import get_user_model

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
