from rest_framework import serializers

from apps.users.models import UserChat


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ('user', 'chat_id',)
