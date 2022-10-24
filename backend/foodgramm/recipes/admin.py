from django.contrib import admin
from .models import Ingridient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'description',
        'time'
    )
    list_editable = ('title', 'description', 'time')
    search_fields = ('title',)
    list_filter = ('time',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'colour',
        'slug'
    )
    list_editable = ('title', 'colour', 'slug')
    search_fields = ('title',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'quantity',
        'measure_unit'
    )
    list_editable = ('title', 'quantity', 'measure_unit')
    search_fields = ('title',)
    list_filter = ('measure_unit',)
    empty_value_display = '-пусто-'
