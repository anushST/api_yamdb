from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.SET_NULL,
        verbose_name='Отзыв',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        help_text='Идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Категория',
        help_text='Идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        help_text='Целое число в диапазоне от 1 до 10'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title[:50]


class Comment(models.Model):
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
    text = models.TextField(
        verbose_name='Комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.review)
