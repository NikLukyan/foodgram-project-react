# Generated by Django 3.2 on 2023-05-18 13:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Количество должно быть больше 0.')], verbose_name='Количество ингредиента в рецепте'),
        ),
    ]
