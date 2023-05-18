from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearchFilter, CustomRecipeFilterSet
from api.pagination import RecipeUserPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    UserSerializer,
    NewUserSerializer,
    SetPasswordSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateUpdateSerializer,
    SubscriptionsSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    FavoriteRecipeUser,
    ShoppingCartUser
)
from users.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)
    pagination_class = RecipeUserPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return NewUserSerializer
        return UserSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False,
            methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if check_password(request.data['current_password'], user.password):
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

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            data=pages,
            many=True,
            context={
                'request': request
            },
        )
        serializer.is_valid()
        return self.get_paginated_response(data=serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        """Метод обрабатывающий эндпоинт subscribe."""
        interest_user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if request.user == interest_user:
                return Response(
                    {'errors': 'Невозможно подписаться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            Follow.objects.create(following=interest_user, user=request.user)
            serializer = SubscriptionsSerializer(
                interest_user,
                context={
                    'request': request
                },
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscribe = Follow.objects.filter(
            following=interest_user,
            user=request.user
        )
        if subscribe:
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': (
                    'Вы не были подписаны на пользователя '
                    + f'{interest_user.username}.'
            )},
            status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    permission_classes = (AllowAny,)


def post_delete_relationship_user_with_object(request, pk, model, message):
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
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
        text = {
            'id': recipe.id,
            'name': recipe.name,
            'image': str(recipe.image),
            'cooking_time': recipe.cooking_time
        }
        return Response(text, status=status.HTTP_201_CREATED)
    obj_recipe = model.objects.filter(
        recipe=recipe,
        user=request.user
    )
    if obj_recipe:
        obj_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'errors': f'Рецепта с номером {pk} нет у Вас в {message}.'},
        status=status.HTTP_400_BAD_REQUEST
    )


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipeUserPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilterSet
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """Ветвление пермишенов."""
        if self.action in ['list', 'retrieve']:
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True,
            methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        return post_delete_relationship_user_with_object(
            request=request,
            pk=pk,
            model=FavoriteRecipeUser,
            message='избранном'
        )

    @action(detail=True,
            methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        return post_delete_relationship_user_with_object(
            request=request,
            pk=pk,
            model=ShoppingCartUser,
            message='списке покупок'
        )

    @action(detail=False,
            methods=['get'])
    def download_shopping_cart(self, request):
        recipes_user_in_shoplist = ShoppingCartUser.objects.filter(
            user=request.user
        )
        recipes = Recipe.objects.filter(
            recipe_in_shoplist__in=recipes_user_in_shoplist
        )
        ingredients = Ingredient.objects.filter(
            ingredient_in_recipe__recipe__in=recipes
        )
        queryset_ingredients = ingredients.annotate(
            sum_amount_ingredients=(Sum('ingredient_in_recipe__amount'))
        )
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
        filename = 'my_shopping_cart.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename
        )
        return response
