from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    date_time = models.DateTimeField(
        verbose_name="Дата",
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-date_time']

    def __str__(self):
        return self.title
