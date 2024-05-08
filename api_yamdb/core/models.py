"""Base models for yamdb project."""
from django.db import models


class BaseModel(models.Model):
    """Base model for Reviews models."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Слаг', max_length=50, unique=True, help_text='Идентификатор'
    )

    class Meta:
        """Meta options for BaseModel."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.name
