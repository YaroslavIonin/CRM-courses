from django.db import models


class Enrollment(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        to='courses.Lesson',
        on_delete=models.CASCADE,
        null=True,
        related_name='enrollments',
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f'{self.user} - {self.lesson}'
