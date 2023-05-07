from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.db import models

from .validators import validate_username


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    """Описание нестандартной модели пользователя."""
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
        # validators=[validate_password],
    )
    # auth_token = models.CharField(
    #     verbose_name='Токен',
    #     max_length=254,
    #     blank=True,
    #     null=True,
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""
        return self.email

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRole.USER


class Follow(models.Model):
    """Описание модели подписки на автора рецепта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецептов',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_user_author',
                fields=['user', 'following'],
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return 'Пользователь {} подписан на {}'.format(
            self.user,
            self.following
        )
