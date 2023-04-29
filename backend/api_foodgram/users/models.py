from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username, validate_email


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя',
        validators=[UnicodeUsernameValidator, validate_username]
    )
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True,
        verbose_name='Почтовый адрес',
        validators=[validate_email]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
    )
    role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль',
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )
    auth_token = models.CharField(
        verbose_name='Токен',
        max_length=254,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRole.USER
