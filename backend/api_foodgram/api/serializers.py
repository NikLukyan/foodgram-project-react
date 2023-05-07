from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from users.models import Follow


User = get_user_model()


def user_is_subscribed(self, obj):
    """Подписан ли текущий пользователь на другого пользователя."""
    user = self.context['request'].user
    if user.is_anonymous:
        return False
    return Follow.objects.filter(user=user, following=obj.pk).exists()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Подписан ли текущий пользователь на другого пользователя."""
        return user_is_subscribed(self, obj)


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def validate_password(self, value):
        """Проверка пароля."""
        return make_password(value)


class SetPasswordSerializer(serializers.Serializer):
    """Сериализатор установки пароля."""
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
