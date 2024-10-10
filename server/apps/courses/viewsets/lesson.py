from datetime import datetime
from typing import Type

from rest_framework import viewsets, serializers

from apps.courses.models import Lesson
from apps.courses.serializers import LessonSerializer, CreateLessonSerializer


class LessonViewSet(viewsets.ModelViewSet):

    SERIALIZER_CLASS_MAP = {
        'list': LessonSerializer,
        'create': CreateLessonSerializer,
    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(self.action, LessonSerializer)

    def get_queryset(self) -> Type[list[Lesson]]:
        return Lesson.objects.filter(
            date__gte=datetime.now(),
        )
