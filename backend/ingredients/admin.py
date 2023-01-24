from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_editable = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'
