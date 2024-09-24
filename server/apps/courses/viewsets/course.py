from typing import Type

from rest_framework import viewsets, serializers

from apps.courses.models import Course
from apps.courses.permissions import IsOperatorOrReadOnly
from apps.courses.serializers import CreateCourseSerializer, CourseSerializer, UpdateCourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOperatorOrReadOnly]

    SERIALIZER_CLASS_MAP = {
        'list': CourseSerializer,
        'create': CreateCourseSerializer,
        'update': UpdateCourseSerializer,
    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(self.action, CourseSerializer)

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset
