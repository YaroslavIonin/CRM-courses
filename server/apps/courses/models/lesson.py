from django.db import models

from .course import Course
from .enrollment import Enrollment


class Lesson(models.Model):
    date = models.DateField(
        verbose_name="Дата занятия",
    )
    time_start = models.TimeField(
        verbose_name='Начало в',
    )
    time_finish = models.TimeField(
        verbose_name='Окончание в',
    )
    max_count_enrollments = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество записей',
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
    )

    @property
    def current_count_enrollments(self):
        return Enrollment.objects.filter(
            lesson=self,
        ).count()

    def is_available(self):
        return self.current_count_enrollments < self.max_count_enrollments

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-date']

    def __str__(self):
        return f'{self.course.title} ({self.date})'
