# Generated by Django 3.2 on 2023-05-04 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auth_token',
        ),
    ]