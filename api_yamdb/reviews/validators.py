"""Validators for reviews app."""
import datetime

from django.core.validators import MaxValueValidator


def get_current_year_validator(value):
    """Return current year validator."""
    return MaxValueValidator(datetime.datetime.now().year)(value)
