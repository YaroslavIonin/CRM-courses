from django.contrib import admin

from apps.users.models import UserChat


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    pass
