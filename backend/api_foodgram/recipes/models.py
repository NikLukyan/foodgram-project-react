from django.db import models
from django.contrib.auth import get_user_model

from recipes.validators import hex_field_validator
# from users.models import User

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=200,
        verbose_name='Тег',
        help_text='Введите название тега',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        help_text='Введите цвет',
        validators=[hex_field_validator]

    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг тега',
        help_text='Введите слаг тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Ингредиент',
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Введите название единицы измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        through='TagRecipe',
        through_fields=('recipe', 'tag'),
        verbose_name='Список тегов',
        related_name='recipes',
    )
    # author = models.ForeignKey(
    #     User,
    #     blank=False,
    #     null=False,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор рецепта',
    # )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Список ингредиентов',
        related_name='recipes',
    )
#     is_favorited = models.BooleanField(
#         verbose_name='Находится ли в избранном',
#     )
#     is_in_shopping_cart = models.BooleanField(
#         verbose_name='Находится ли в корзине',
#     )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.CharField(
        max_length=200,
        verbose_name='Ссылка на картинку на сайте',
        help_text='Загрузите ссылку на картинку к рецепту',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Введите время приготовления (в минутах)',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user_id', 'recipe_id'],
        #         name='unique_recipe',
        #     )
        # ]

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    """Модель отношения Тег-Рецепт."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class IngredientRecipe(models.Model):
    """Модель отношения Ингредиент-Рецепт."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
