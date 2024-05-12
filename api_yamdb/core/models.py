"""Base models for yamdb project."""
from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG, MAX_LENGTH_TEXT

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    """Base model for Category and Genre models."""

    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(
        'Слаг', max_length=MAX_LENGTH_SLUG,
        unique=True, help_text='Идентификатор'
    )

    class Meta:
        """Meta options for BaseModel."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.name


class ReviewCommentBaseModel(models.Model):
    """Base model for Review and Comment models."""

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    pub_date = models.DateTimeField('Дата и время', auto_now_add=True)

    class Meta:
        """Meta options for BaseModel."""

        abstract = True
        ordering = ["-pub_date"]

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.text[:MAX_LENGTH_TEXT]
