"""Module for application configuration."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Django application configuration class for the Core app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
