from django.urls import include, path, re_path
from rest_framework import routers

from .views import (
    UserViewSet,
    TagViewSet,
    IngredientViewSet, RecipeViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
