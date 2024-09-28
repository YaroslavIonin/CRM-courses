from django.db import models


class Enrollment(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        to='courses.Course',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        # ordering = ['-course.date_time']

    def __str__(self):
        return self.course.title
