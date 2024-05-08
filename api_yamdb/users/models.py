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

    email = models.EmailField('Email-адрес', unique=True, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=9, choices=UsersType.choices, default=UsersType.USER)
    is_admin = models.BooleanField('Админ', default=False)

    def save(self, *args, **kwargs):
        """Save the current instance.

        Ovverided to automaticly set field is_admin True to superuser.
        """
        if self.is_superuser or self.role == self.UsersType.ADMIN:
            self.is_admin = True
        super().save(*args, **kwargs)

    class Meta:
        """Meta-data of the User class."""

        ordering = ('id',)


class ConfirmationCode(models.Model):
    """Confirmation codes of users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='code_user')
    code = models.PositiveIntegerField()
