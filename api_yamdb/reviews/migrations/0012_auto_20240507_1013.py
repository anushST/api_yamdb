# Generated by Django 3.2 on 2024-05-07 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20240507_1003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]
