# Generated by Django 3.2 on 2023-04-30 12:30

import django.contrib.auth.password_validation
import django.core.validators

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230430_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='Почтовый адрес'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, validators=[django.contrib.auth.password_validation.validate_password], verbose_name='Пароль'),
        ),
    ]
