from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from recipes.validators import hex_field_validator, slug_field_validator

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
    color = ColorField(
        format='hex',
        default='#FF0000',
        verbose_name='Цветовой HEX-код',
        help_text='Цветовой HEX-код',
        validators=[hex_field_validator])

    slug = models.SlugField(
        unique=True,
        db_index=True,
        max_length=200,
        verbose_name='Слаг тега',
        help_text='Введите слаг тега',
        validators=[slug_field_validator]
    )

    class Meta:
        ordering = ['id']
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
        verbose_name='Список тегов',
        help_text='Список тегов',
        related_name='tags_recipes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Автор рецепта',
        related_name='author_recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        help_text='Ингредиенты для приготовления блюда',
        related_name='ingredients_recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        verbose_name='Ссылка на картинку',
        help_text='Загрузите ссылку на картинку к рецепту',
        upload_to='recipes',
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты!'
            ),
            MaxValueValidator(
                600, 'Время приготовления не может быть более 10 часов!'
            )
        ],
        default=1,
        verbose_name='Время приготовления в минутах',
        help_text='Время приготовления в минутах',
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
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество должно быть больше 0.'
            ),
            MaxValueValidator(
                limit_value=1000,
                message='Количество ингредиентов не может быть больше 1000!'
            )
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


class ShoppingCartUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_in_shoplist',
        verbose_name='Пользователь, имеющий рецепт в cписке покупок',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_shoplist',
        verbose_name='Рецепт из списка покупок пользователя',
        help_text='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                name='unique_user_shoplist',
                fields=['user', 'recipe'],
            ),
        ]

    def __str__(self):
        return 'У {} в списке покупок рецепт: {}'.format(
            self.user,
            self.recipe
        )


class FavoriteRecipeUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь, имеющий избранные рецепты',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранный рецепт определенного пользователя',
        help_text='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                name='unique_favorite_recipe_user',
                fields=['user', 'recipe'],
            ),
        ]

    def __str__(self):
        return 'У {} в избранном рецепт: {}'.format(
            self.user,
            self.recipe
        )
