"""Models of "users" app."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    class UsersType(models.TextChoices):
        """Users type options."""

        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=9, choices=UsersType.choices, default=UsersType.USER)
