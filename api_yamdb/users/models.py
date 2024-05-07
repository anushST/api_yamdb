"""Models of "users" app."""
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .constants import NOT_ALLOWED_NAMES_FOR_USERS


class User(AbstractUser):
    """Custom user model."""

    class UsersType(models.TextChoices):
        """Users type options."""

        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField('Email-адрес', unique=True, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=9, choices=UsersType.choices, default=UsersType.USER)

    def save(self, *args, **kwargs):
        """Save the current instance.

        Overrided to not allow to save usernames from
        NOT_ALLOWED_NAMES_FOR_USERS constant.
        """
        if self.username in NOT_ALLOWED_NAMES_FOR_USERS:
            raise ValidationError('Нельзя использовать это имя в username.')
        super().save(*args, **kwargs)

    class Meta:
        """Meta-data of the User class."""

        ordering = ('id',)


class ConfirmationCode(models.Model):
    """Confirmation codes of users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='code_user')
    code = models.PositiveIntegerField()
