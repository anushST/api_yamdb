# Generated by Django 3.2 on 2024-05-08 15:06

import django.core.validators
from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_alter_title_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-1000), reviews.validators.get_current_year_validator], verbose_name='Год выпуска'),
        ),
    ]
