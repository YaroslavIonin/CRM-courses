from rest_framework import generics

from apps.users.models import UserChat
from apps.users.serializers import UserChatSerializer


class UserChatRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserChatSerializer
    queryset = UserChat.objects.all()

    def get_object(self):
        return UserChat.objects.get_or_create(
            user=self.request.user,
            chat_id=self.kwargs['chat_id'],
        )[0]
