from django.contrib import admin

from .models import Favorite, InShopCart, Recipe


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        RecipeIngredientsInline,
    )
    exclude = (
        'ingredients',
    )
    list_display = (
        'pk',
        'author',
        'name',
        'count_favorite',
        'text'
    )
    filter_horizontal = ('tags',)
    list_filter = (
        'name',
        'author',
        'tags'
    )
    list_editable = (
        'author',
        'name',
        'text'
    )
    empty_value_display = '-пусто-'

    def count_favorite(self, obj):
        return Recipe.objects.filter(fav_recipes__recipe=obj).count()
    count_favorite.short_description = 'Кол-во добавлений в избранное'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = (
        'user',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


@admin.register(InShopCart)
class InShopCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = (
        'user',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
