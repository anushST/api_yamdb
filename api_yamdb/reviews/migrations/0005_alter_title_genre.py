# Generated by Django 3.2 on 2024-05-03 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_title_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]
