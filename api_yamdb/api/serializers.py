"""Serializers for api app."""
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


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


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    rating = serializers.IntegerField(required=False)

    class Meta:
        """Meta-data of TitleSerializier class."""

        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)

    def to_representation(self, instance):
        """
        Let`s override to_representation method.

        Custom data representation when serializing responses.
        """
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance.genre, many=True).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation


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

    def validate(self, data):
        """Let`s override validate method."""
        if self.context['request'].method != 'PATCH':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context['request'].user
            if Review.objects.filter(title_id=title_id,
                                     author=author).exists():
                raise serializers.ValidationError(
                    "Review for this title already exists.")
        return data


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
