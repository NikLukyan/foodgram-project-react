from django.contrib import admin

from .models import (
    Ingredient,
    FavoriteRecipeUser,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCartUser,
    Tag,
)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'num_favorite_recipes',)
    list_filter = ('author', 'name', 'tags',)
    inlines = [RecipeTagInline, RecipeIngredientInline, ]

    def num_favorite_recipes(self, obj):
        return FavoriteRecipeUser.objects.filter(recipe=obj).count()

    class Meta:
        model = Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)



class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FavoriteRecipeUser)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCartUser)
admin.site.register(Tag, TagAdmin)
