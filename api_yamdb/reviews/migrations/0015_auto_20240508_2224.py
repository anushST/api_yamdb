# Generated by Django 3.2 on 2024-05-08 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_alter_title_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='name',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='slug',
        ),
    ]
