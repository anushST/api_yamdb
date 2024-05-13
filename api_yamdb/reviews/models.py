"""Models for review app."""
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (MAX_LENGTH_NAME, MIN_SCORE, MAX_SCORE)
from .validators import YearValidator
from core.models import CategoryGenreBaseModel, ReviewCommentBaseModel

User = get_user_model()


class Title(models.Model):
    """The Title model."""

    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=[YearValidator()]
    )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, verbose_name='Категория',
        null=True
    )

    class Meta:
        """Meta-data of Title model."""

        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.name


class Genre(CategoryGenreBaseModel):
    """The Genre model."""

    class Meta(CategoryGenreBaseModel.Meta):
        """Meta-data of Genre model."""

        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(CategoryGenreBaseModel):
    """The Category model."""

    class Meta(CategoryGenreBaseModel.Meta):
        """Meta-data of Category model."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Review(ReviewCommentBaseModel):
    """The Review model."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        help_text=f'Целое число в диапазоне от {MIN_SCORE} до {MAX_SCORE}',
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ])

    class Meta(ReviewCommentBaseModel.Meta):
        """Meta-data of Review model."""

        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = [['title', 'author']]


class Comment(ReviewCommentBaseModel):
    """The Comment model."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBaseModel.Meta):
        """Meta-data of Comment model."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
