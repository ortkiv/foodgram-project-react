from django.contrib import admin
from .models import Ingridient, Recipe, Tag


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
        'text',
        'image',
        'cooking_time'
    )
    list_editable = ('name', 'text', 'image', 'cooking_time',)
    search_fields = ('name',)
    list_filter = ('cooking_time',)
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
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    list_display = (
        'pk',
        'name',
        'quantity',
        'measurement_unit'
    )
    list_editable = ('name', 'quantity', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'