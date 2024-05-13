"""Models of "users" app."""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .constants import ROLE_MAX_LENGTH, USERNAME_MAX_LENGTH
from .validators import validate_username


class User(AbstractUser):
    """Custom user model."""

    class UsersType(models.TextChoices):
        """Users type options."""

        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        'username',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text=('Не более 150 символов. Только буквы,  '
                   'цифры и @/./+/-/_ только.'),
        validators=(UnicodeUsernameValidator(), validate_username),
        error_messages={
            'unique': "Пользователь с таким именем уже сеществует.",
        },
    )
    email = models.EmailField('Email-адрес', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH, choices=UsersType.choices,
        default=UsersType.USER)

    @property
    def is_admin(self) -> bool:
        """Check is the user admin."""
        return (self.is_superuser or self.role == self.UsersType.ADMIN
                or self.is_staff)

    @property
    def is_moderator(self) -> bool:
        """Check is the user moderator."""
        return self.role == self.UsersType.MODERATOR

    class Meta:
        """Meta-data of the User class."""

        ordering = ('id',)
