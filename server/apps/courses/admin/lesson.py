from django.contrib import admin

from ..models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
