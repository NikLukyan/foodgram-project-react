from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from recipes.validators import hex_field_validator, slug_field_validator
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
        verbose_name='HEX цвет',
        help_text='Введите цвет в формате HEX',
        validators=[hex_field_validator]

    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        max_length=200,
        verbose_name='Слаг тега',
        help_text='Введите слаг тега',
        validators=[slug_field_validator]
    )

    class Meta:
        ordering = ['slug']
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
        through='RecipeTag',
        through_fields=('recipe', 'tag'),
        verbose_name='Список тегов',
        # related_name='tags_recipes',
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор рецепта',
    # )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Список ингредиентов',
        related_name='ingredients_recipes',
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
    image = models.ImageField(
        verbose_name='Ссылка на картинку',
        help_text='Загрузите ссылку на картинку к рецепту',
        upload_to='recipe',
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Введите время приготовления (в минутах)',
        validators=[MinValueValidator(
            limit_value=1,
            message='Минимальное время приготовления - 1 минута.')
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]


class RecipeTag(models.Model):
    """Модель отношения Тег-Рецепт."""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Связь тега c рецептом'
        verbose_name_plural = 'Связи тегов c рецептами'
        constraints = [
            models.UniqueConstraint(
                name='unique_tag_recipe',
                fields=['tag', 'recipe'],
            ),
        ]

    def __str__(self):
        return 'Тег {} в рецепте {}'.format(
            self.tag,
            self.recipe
        )


class RecipeIngredient(models.Model):
    """Модель отношения Ингредиент-Рецепт."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Рецепт',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента в рецепте',
        validators=[MinValueValidator(
            limit_value=1,
            message='Количество должно быть больше 0.')
        ],
    )

    class Meta:
        verbose_name = 'Связь ингредиента c рецептом'
        verbose_name_plural = 'Связи ингредиентов c рецептами'
        constraints = [
            models.UniqueConstraint(
                name='unique_ingredient_recipe',
                fields=['ingredient', 'recipe'],
            ),
        ]

    def __str__(self):
        return 'Ингридиент {} в рецепте {}'.format(
            self.ingredient,
            self.recipe
        )
