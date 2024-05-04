import os
import django
import csv
from django.db import transaction
from django.utils.dateparse import parse_datetime

# Надо имеено в таком порядке, иначе не работает
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")
django.setup()

from users.models import User
from reviews.models import Title, Category, Review, Comment, Genre


# Описываем пути к файлам данных
CSV_FILES_PATHS = {
    'users': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/users.csv',
    'categories': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/category.csv',
    'titles': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/titles.csv',
    'review': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/review.csv',
    'comments': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/comments.csv',
    'genre': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/genre.csv',
    'genre_title': '/home/ubuntu/Dev/api_yamdb/api_yamdb/static/data/genre_title.csv',
}

# Унифицированная функция для импорта данных из CSV
def import_from_csv(file_path, create_function):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            with transaction.atomic():
                create_function(row)

# Примеры функций создания объектов моделей
def create_user(row):
    User.objects.create(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        role=row['role']
    )

def create_category(row):
    Category.objects.create(
        id=row['id'],
        name=row['name'],
        slug=row['slug'],
    )

def create_title(row):
    category = Category.objects.get(id=row['category'])
    Title.objects.create(
        id=row['id'],
        name=row['name'],
        year=row['year'],
        category=category
    )


def create_review(row):
    title = Title.objects.get(id=row['title_id'])
    author = User.objects.get(id=row['author'])
    pub_date = parse_datetime(row['pub_date'])

    Review.objects.create(
        id=row['id'],
        title=title,
        text=row['text'],
        author=author,
        score=row['score'],
        pub_date=pub_date
    )


def create_comments(row):
    review = Review.objects.get(id=row['review_id'])
    author = User.objects.get(id=row['author'])
    pub_date = parse_datetime(row['pub_date'])

    Comment.objects.create(
        id=row['id'],
        review=review,
        text=row['text'],
        author=author,
        pub_date=pub_date
    )


def create_genre(row):
    Genre.objects.create(
        id=row['id'],
        name=row['name'],
        slug=row['slug']
    )


def create_genre_title(row):
    title = Title.objects.get(id=row['title_id'])
    genre = Genre.objects.get(id=row['genre_id'])
    title.genre.add(genre)


if __name__ == '__main__':
    # Удаляем существующие данные
    User.objects.all().delete()
    Title.objects.all().delete()
    Category.objects.all().delete()
    Review.objects.all().delete()
    Comment.objects.all().delete()
    Genre.objects.all().delete()

    # Запускаем импорт данных    
    import_from_csv(CSV_FILES_PATHS['users'], create_user)
    import_from_csv(CSV_FILES_PATHS['categories'], create_category)
    import_from_csv(CSV_FILES_PATHS['titles'], create_title)
    import_from_csv(CSV_FILES_PATHS['review'], create_review)
    import_from_csv(CSV_FILES_PATHS['comments'], create_comments)
    import_from_csv(CSV_FILES_PATHS['genre'], create_genre)
    import_from_csv(CSV_FILES_PATHS['genre_title'], create_genre_title)
