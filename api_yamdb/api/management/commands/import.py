"""Import csv files to database."""
import csv
from django.core.management.base import BaseCommand
from reviews.models import Title, Genre, Category, Review, Comment
from users.models import User

data_files = {
    'users': 'static/data/users.csv',
    'category': 'static/data/category.csv',
    'titles': 'static/data/titles.csv',
    'review': 'static/data/review.csv',
    'comments': 'static/data/comments.csv',
    'genre': 'static/data/genre.csv',
    'genre_title': 'static/data/genre_title.csv',
}


class Command(BaseCommand):
    """Command for import csv into database."""

    help = 'Import csv files to database.'

    def handle(self, *args, **options):
        """Handle function."""
        for model, file_path in data_files.items():
            print(f'Importing {file_path} to {model}...')
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    obj = self.create_object(model, row)
                    if obj:
                        obj.save()
            print(f'Success import {file_path}.')

    def create_object(self, model_name, data):
        """Create object from django ORM."""
        if model_name == 'users':
            return User(**data)
        elif model_name == 'category':
            return Category(**data)
        elif model_name == 'titles':
            category = Category.objects.get(id=data['category'])
            data['category'] = category
            return Title(**data)
        elif model_name == 'review':
            author = User.objects.get(id=data['author'])
            title = Title.objects.get(id=data['title_id'])
            data['author'] = author
            data['title'] = title
            return Review(**data)
        elif model_name == 'comments':
            author = User.objects.get(id=data['author'])
            review = Review.objects.get(id=data['review_id'])
            data['author'] = author
            data['review'] = review
            return Comment(**data)
        elif model_name == 'genre':
            return Genre(**data)
        elif model_name == 'genre_title':
            title = Title.objects.get(id=data['title_id'])
            genre = Genre.objects.get(id=data['genre_id'])
            title.genre.add(genre)
