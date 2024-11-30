from django.contrib import admin

from ..models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'course__title',
        'course__author',
        'date',
        'time_start',
        'time_finish',
    ]
    list_filter = [
        'course__title',
        'course__author',
    ]
