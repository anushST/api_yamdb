"""Base models for yamdb project."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    """Base model for Category and Genre models."""

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

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.text[:50]
