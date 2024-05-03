from rest_framework.serializers import ModelSerializer

from reviews.models import Title, Genre, Category, Review, Comment, User


class TitleSerializer(ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'title', 'score', 'author', 'pub_date')


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('review', 'author', 'text', 'pub_date')
