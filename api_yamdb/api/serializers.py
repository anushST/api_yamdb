"""Serializers for api app."""
from rest_framework import serializers

from reviews.models import Title, Genre, Category, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model."""

    class Meta:
        """Meta-data of TitleSerializier class."""

        model = Title
        fields = ('name', 'year', 'rating',
                  'description', 'genre', 'category',)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        """Meta-data of GenreSerializier class."""

        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        """Meta-data of CategorySerializier class."""

        model = Category
        fields = ('name', 'slug',)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Meta-data of ReviewSerializier class."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Meta-data of CommentSerializier class."""

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
