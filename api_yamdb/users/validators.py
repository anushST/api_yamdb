"""Validators of users app."""
from django.core.exceptions import ValidationError

from .constants import NOT_ALLOWED_NAMES_FOR_USERS


def validate_username(value):
    """Validate username field.

    Username can't be set a value which in NOT_ALLOWED_NAMES_FOR_USERS
    """
    if value in NOT_ALLOWED_NAMES_FOR_USERS:
        raise ValidationError('Нельзя использовать это имя в username.')
