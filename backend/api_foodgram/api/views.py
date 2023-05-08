from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import UserPagination
from api.serializers import (
    UserSerializer,
    NewUserSerializer, SetPasswordSerializer, TagSerializer)
from recipes.models import Tag

User = get_user_model()


class ListRetrieveModelViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """
    Кастомный базовый вьюсет:
    Вернуть список объектов (GET);
    Вернуть объект (GET);
    """
    pass

class UserViewSet(viewsets.ModelViewSet):
    """Представление для модели User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # search_fields = ('username',)
    permission_classes = (IsAuthenticated,)
    pagination_class = UserPagination
    # lookup_field = 'username'

    def get_permissions(self):
        """Ветвление пермишенов."""
        # Если GET-list или POST запрос
        if self.action == 'list' or self.action == 'create':
            # Можно все
            return (AllowAny(),)
        # Для остальных ситуаций оставим текущий
        # перечень пермишенов без изменений
        return super().get_permissions()

    def get_serializer_class(self):
        """Ветвление сериализаторов."""
        # При создании нового пользователя, выбираем другой сериализатор
        if self.action == 'create':
            return NewUserSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Метод обрабатывающий эндпоинт me."""
        user = get_object_or_404(User, email=request.user.email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        """Метод обрабатывающий эндпоинт set_password."""
        user = get_object_or_404(User, email=request.user.email)
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if check_password(request.data['current_password'], user.password):
                # хешируем новый пароль
                new_password = make_password(request.data['new_password'])
                user.password = new_password
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'current_password': 'Вы ввели неверный пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ListRetrieveModelViewSet):
    """Представление для модели Tag"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

