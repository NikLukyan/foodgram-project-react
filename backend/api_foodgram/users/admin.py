from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = ('email', 'username',)
    list_filter = ('is_superuser',)


admin.site.register(User, UserAdmin)
