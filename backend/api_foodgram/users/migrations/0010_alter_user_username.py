# Generated by Django 3.2 on 2023-05-18 09:03

import django.contrib.auth.validators
import users.validators

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20230517_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), users.validators.validate_username], verbose_name='Логин пользователя'),
        ),
    ]
