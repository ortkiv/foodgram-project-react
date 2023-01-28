from django.contrib import admin
from django.contrib.auth import get_user_model, models

from .forms import CustomUserCreationForm
from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'email',
        'is_superuser',
        'is_active'
    )
    list_editable = (
        'first_name',
        'last_name',
        'is_active',
    )
    search_fields = (
        'username',
    )
    list_filter = (
        'username',
        'email'
    )
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


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
