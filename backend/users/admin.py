from django.contrib import admin
from django.contrib.auth import get_user_model, models

from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'is_superuser',
        'is_active'
    )
    list_editable = (
        'password',
        'first_name',
        'last_name',
        'is_active'
    )
    search_fields = ('username',)
    list_filter = (
        'first_name',
        'email'
    )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    list_editable = (
        'user',
        'author'
    )
    search_fields = ('user',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.unregister(models.Group)
