from rest_framework.serializers import ModelSerializer

from reviews.models import Title, Genre, Category


class TitleSerializer(ModelSerializer):

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating',
                  'description', 'genre', 'category',)


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)

