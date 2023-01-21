from django.contrib import admin
from django.contrib.auth import get_user_model, models

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'first_name', 'last_name', 'email',
        'password', 'is_superuser', 'is_active'
    )
    list_editable = ('password', 'first_name', 'last_name', 'is_active')
    list_filter = ('first_name', 'email',)
    empty_value_display = '-пусто-'


admin.site.unregister(models.Group)
