from django.urls import path
from django.contrib import admin
from django.shortcuts import render, redirect

from apps.courses.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'course',
        'date',
        'course__author',
        'count_left_enrollments',
    ]
    list_filter = [
        'course__author',
        'course__title',
    ]
    actions = ['to_calendar']

    @admin.display(description='Автор')
    def course__author(self, obj):
        return obj.course.author

    @admin.display(description='Свободных мест', )
    def count_left_enrollments(self, obj):
        return obj.count_left_enrollments

    @admin.action(description='Отобразить календарь')
    def to_calendar(self, request, queryset):
        lessons = [
            {
                'title': str(lesson.course.title),
                'date': str(lesson.date),
                'time_start': str(lesson.time_start),
                'time_finish': str(lesson.time_finish),
            }
            for lesson in queryset
        ]
        request.session['lessons'] = lessons
        return redirect('admin:lesson_calendar')

    def calendar_view(self, request):
        lessons = request.session.get('lessons', [])

        if 'lessons' in request.session:
            del request.session['lessons']

        return render(
            request,
            "admin/lesson_calendar.html",
            {'lessons': lessons},
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'calendar/',
                self.calendar_view,
                name='lesson_calendar'
            ),
        ]
        return custom_urls + urls
