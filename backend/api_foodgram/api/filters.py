from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class CustomRecipeFilterSet(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        label='tags',
        queryset=Tag.objects.all()
    )
    author = AllValuesMultipleFilter(field_name='author__id')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def _bool_filter(self, key, value, queryset, user):
        """Фильтрация для логических ключей."""
        map_dict = {f'{key}__user': user}
        if not user.is_anonymous:
            if value is True:
                return queryset.filter(**map_dict)
            return queryset.exclude(**map_dict)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        key = 'favorite_recipes'
        return self._bool_filter(key, value, queryset, user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        key = 'recipe_in_shoplist'
        return self._bool_filter(key, value, queryset, user=self.request.user)

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
