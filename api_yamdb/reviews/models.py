"""Models for review app."""
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import ROUND_FUC_ARGS, MIN_YEAR_FOR_ART_OF_HUMAN
from core.models import BaseModel
from .validators import get_current_year_validator

User = get_user_model()


class Round(models.Func):
    """Call round function from SQL."""

    function = 'ROUND'
    arity = ROUND_FUC_ARGS


class RatingQuerySet(models.QuerySet):
    """Rating queryset."""

    def with_rating(self):
        """Return rounded rating."""
        return self.annotate(
            rating_avg=Round(models.Avg('reviews__score'),
                             ROUND_FUC_ARGS, output_field=models.FloatField()))


class Title(models.Model):
    """The Title model."""

    name = models.CharField('Название', max_length=256)
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(MIN_YEAR_FOR_ART_OF_HUMAN),
            get_current_year_validator
        ]
    )
    objects = RatingQuerySet.as_manager()

    @property
    def rating(self):
        """Rating atribute."""
        return getattr(self, 'rating_avg', None)

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


class Genre(BaseModel):
    """The Genre model."""

    class Meta(BaseModel.Meta):
        """Meta-data of Genre model."""

        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """The Category model."""

    class Meta(BaseModel.Meta):
        """Meta-data of Category model."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Review(models.Model):
    """The Review model."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        'Оценка', help_text='Целое число в диапазоне от 1 до 10',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ])
    pub_date = models.DateTimeField(
        'Дата и время отзыва', auto_now_add=True)

    class Meta:
        """Meta-data of Review model."""

        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = [['title', 'author']]

    def __str__(self):
        """Magic method to display information about a class object."""
        return self.title[:50]


class Comment(models.Model):
    """The Comment model."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField(
        'Дата и время комментария',
        auto_now_add=True
    )

    class Meta:
        """Meta-data of Comment model."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Magic method to display information about a class object."""
        return str(self.review)
