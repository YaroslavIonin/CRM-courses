from django.contrib import admin

from ..models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'phone_number',
        'is_operator',
    ]
    fields = (
        'username',
        'phone_number',
        'is_operator',
        'is_superuser',
    )
