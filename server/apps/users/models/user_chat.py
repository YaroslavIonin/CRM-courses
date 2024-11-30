from django.db import models

from apps.users.models import User


class UserChat(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )
    chat_id = models.CharField(
        max_length=255,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.user.username}: {self.chat_id}"
