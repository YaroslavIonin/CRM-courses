from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        verbose_name='Никнейм'
    )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        region='RU',
        unique=True,
        verbose_name='Номер телефона',
    )
    is_operator = models.BooleanField(
        default=False,
        verbose_name='Оператор'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username}'
