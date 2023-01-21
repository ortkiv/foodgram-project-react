from django.contrib import admin

from .models import Favorite, Follow, Ingridient, InShopCart, Recipe, Tag


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeTagInline, RecipeIngredientsInline]
    exclude = ['tags', 'ingredients']
    list_display = (
        'pk',
        'author',
        'name',
        'count_favorite',
        'text'
    )

    def count_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    count_favorite.short_description = 'Кол-во добавлений в избранное'
    list_editable = ('author', 'name', 'text',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [RecipeTagInline]
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_editable = ('name', 'color', 'slug')
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_editable = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    list_editable = ('user', 'author')
    search_fields = ('user',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = ('user', 'recipe')
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
    list_editable = ('user', 'recipe')
    search_fields = ('recipe',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
