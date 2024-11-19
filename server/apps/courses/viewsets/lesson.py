from datetime import datetime
from typing import Type

from django.db.models import Count, F
from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters

from apps.courses.models import Lesson, Enrollment
from apps.courses.serializers import LessonSerializer, CreateLessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('course',)

    SERIALIZER_CLASS_MAP = {
        'list': LessonSerializer,
        'create': CreateLessonSerializer,
    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(self.action, LessonSerializer)

    def get_queryset(self) -> Type[list[Lesson]]:
        return Lesson.objects.annotate(
            current_enrollment_count=Count('enrollments')
        ).filter(
            date__gte=datetime.now(),
            max_count_enrollments__gt=F('current_enrollment_count')
        )
