from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'email',
        'role', 'is_superuser', 'is_active'
    )
    search_fields = ('first_name', 'email',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
