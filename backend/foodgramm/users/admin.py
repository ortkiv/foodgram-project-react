from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'email',
        'role', 'is_superuser', 'is_active'
    )
    list_editable = ('role',)
    list_filter = ('first_name', 'email',)
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
