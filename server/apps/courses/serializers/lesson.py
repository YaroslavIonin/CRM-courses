from rest_framework import serializers

from ..models import Lesson
from .course import CourseSerializer


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'date',
            'time_start',
            'time_finish',
            'max_count_enrollments',
            'is_available',
            'course',
        ]


class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'course',
            'date',
            'time_start',
            'time_finish',
            'max_count_enrollments',
        ]

    @property
    def data(self):
        return LessonSerializer(
            instance=self.instance
        ).data
