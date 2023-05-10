from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearchFilter, CustomRecipeFilterSet
from api.pagination import UserPagination, RecipePagination
from api.permissions import AdminAllOnlyAuthorPermission
from api.serializers import (
    UserSerializer,
    NewUserSerializer,
    SetPasswordSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    # RecipeCreateUpdateSerializer,
    RecipeCreateUpdateSerializer,
    SubscriptionsSerializer,
)
from recipes.models import Tag, Ingredient, Recipe, FavoriteRecipeUser, \
    ShoppingCartUser
from users.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Представление для модели User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ('username', 'email')
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

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        """
        Метод обрабатывающий эндпоинт subscriptions.
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        user = request.user
        # объекты пользователей на которых подписан пользователь токена,
        queryset = User.objects.filter(following__user=user)
        # Передаем методу queryset, и возвращаем итерируемый объект,
        # содержащий только данные запрошенной страницы.
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            data=pages,
            many=True,
            context={
                'request': request
            },
        )
        serializer.is_valid()
        # передаем сериализованные данные страницы,
        # и возвращаем экземпляр Response
        return self.get_paginated_response(data=serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        """Метод обрабатывающий эндпоинт subscribe."""
        # получаем интересующего пользователя из url
        interest_user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            # проверяем что подписка происходит не на самого себя
            if request.user == interest_user:
                return Response(
                    {'errors': 'Невозможно подписаться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # проверяем что это будет не повторная подписка на пользователя
            elif Follow.objects.filter(
                    following=interest_user,
                    user=request.user).exists():
                return Response(
                    {'errors': (
                            'Вы уже подписаны на пользователя '
                            + f'{interest_user.username}.'
                    )},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # подписываем пользователя
            Follow.objects.create(following=interest_user, user=request.user)
            # выводим информацию о новой подписке
            serializer = SubscriptionsSerializer(
                interest_user,
                context={
                    'request': request
                },
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # если метод delete
        # проверяем существует ли уже такая подписка
        subscribe = Follow.objects.filter(
            following=interest_user,
            user=request.user
        )
        if subscribe:
            subscribe.delete()
            # удаляем подписку из связующей таблицы, если она там
            return Response(status=status.HTTP_204_NO_CONTENT)
        # иначе говорим что подписки не было
        return Response(
            {'errors': (
                    'Вы не были подписаны на пользователя '
                    + f'{interest_user.username}.'
            )},
            status=status.HTTP_400_BAD_REQUEST
        )

    # @action(
    #     methods=['GET'],
    #     detail=False,
    #     permission_classes=(IsAuthenticated,)
    # )
    # def subscriptions(self, request):
    #     user = request.user
    #     queryset = Subscription.objects.filter(user=user)
    #     page = self.paginate_queryset(queryset)
    #     serializer = SubscriptionSerializer(
    #         page, many=True, context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
    #
    # @action(
    #     methods=['POST', 'DELETE'],
    #     detail=True,
    # )
    # def subscribe(self, request, id):
    #     author = get_object_or_404(User, id=id)
    #     if request.method == 'POST':
    #         serializer = SubscriptionSerializer(
    #             Subscription.objects.create(user=request.user, author=author),
    #             context={'request': request},
    #         )
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED
    #         )
    #     Subscription.objects.filter(user=request.user, author=author).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели тегов"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели ингредиентов"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


def post_delete_relationship_user_with_object(request, pk, model, message):
    """Добавление и удаление рецепта в связующей таблице для пользователя."""
    # получаем рецепт по первичному ключу id
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        # проверяем что это будет не повторное добавление рецепта
        # в связующую таблицу
        if model.objects.filter(
                recipe=recipe,
                user=request.user).exists():
            return Response(
                {'errors': f'Рецепт с номером {pk} уже у Вас в {message}.'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(
            recipe=recipe,
            user=request.user
        )
        # возвращаем ответ
        text = {
            'id': recipe.id,
            'name': recipe.name,
            'image': str(recipe.image),
            'cooking_time': recipe.cooking_time
        }
        return Response(text, status=status.HTTP_201_CREATED)
    # если метод delete
    # проверяем есть ли рецепт в связующей таблице
    obj_recipe = model.objects.filter(
        recipe=recipe,
        user=request.user
    )
    if obj_recipe:
        obj_recipe.delete()
        # удаляем рецепт из связующей таблицы, если он там
        return Response(status=status.HTTP_204_NO_CONTENT)
    # иначе говорим что в не было
    return Response(
        {'errors': f'Рецепта с номером {pk} нет у Вас в {message}.'},
        status=status.HTTP_400_BAD_REQUEST
    )


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для модели рецепта."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilterSet
    permission_classes = (
        IsAuthenticated,
        AdminAllOnlyAuthorPermission,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """Ветвление пермишенов."""
        # Если GET-list или Get-detail запрос
        if self.action in ['list', 'retrieve']:
            return (AllowAny(),)
        # Для остальных ситуаций оставим текущий перечень
        # пермишенов без изменений
        return super().get_permissions()

    def get_serializer_class(self):
        """При создании или обновлении рецепта, выбираем другой сериализатор"""
        if self.action in ['create', 'partial_update', 'update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        """Эндпоинт для избранных рецептов."""
        return post_delete_relationship_user_with_object(
            request=request,
            pk=pk,
            model=FavoriteRecipeUser,
            message='избранном'
        )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        """Эндпоинт для списка покупок."""
        return post_delete_relationship_user_with_object(
            request=request,
            pk=pk,
            model=ShoppingCartUser,
            message='списке покупок'
        )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        """Эндпоинт для загрузки списка покупок."""
        # Выбираем объекты СВЯЗЕЙ пользователя и рецептов из Списка покупок
        # из вспомогательной таблицы
        recipes_user_in_shoplist = ShoppingCartUser.objects.filter(
            user=request.user
        )
        # Выбираем объекты РЕЦЕПТОВ пользователя из Списка покупок
        recipes = Recipe.objects.filter(
            recipe_in_shoplist__in=recipes_user_in_shoplist
        )
        # Выбираем объекты всех ИНГРИДИЕНТОВ
        # у которых в связующей таблице, рецепты равны - рецептам из выборки
        ingredients = Ingredient.objects.filter(
            ingredient_in_recipe__recipe__in=recipes
        )
        # тематически объединяем одинаковые ИНГРИДИЕНТЫ,
        # добавляя аннотацию для каждого объекта
        # сумму количества ингредиентов
        queryset_ingredients = ingredients.annotate(
            sum_amount_ingredients=(Sum('ingredient_in_recipe__amount'))
        )
        # генерация файла со списком ингридиентов
        # для изготовления всех рецептов из списка покупок
        content = (
                'Ваш сервис, Продуктовый помощник, подготовил \nсписок '
                + 'покупок по выбранным рецептам:\n'
                + 50 * '_'
                + '\n\n'
        )
        if not queryset_ingredients:
            content += (
                    'К сожалению, в списке ваших покупок пусто - '
                    + 'поскольку Вы не добавили в него ни одного рецепта.'
            )
        else:
            for ingr in queryset_ingredients:
                content += (
                        f'\t•\t{ingr.name} ({ingr.measurement_unit}) — '
                        + f'{ingr.sum_amount_ingredients}\n\n'
                )
        # Вывод файла
        filename = 'my_shopping_cart.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename
        )
        return response
