"""Validators for reviews app."""
from datetime import datetime

from django.core.exceptions import ValidationError
from .constants import MIN_YEAR_FOR_ART_OF_HUMAN


def validate_year(value):
    """Year validator function."""
    if datetime.now().year < value < MIN_YEAR_FOR_ART_OF_HUMAN:
        raise ValidationError(
            f'Год не может быть меньше {MIN_YEAR_FOR_ART_OF_HUMAN} '
            f'и больше текущего.')
