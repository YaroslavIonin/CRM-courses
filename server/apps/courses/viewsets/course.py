from typing import Type

from rest_framework import viewsets, serializers

from apps.courses.models import Course
from apps.courses.serializers import CreateCourseSerializer, CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):

    SERIALIZER_CLASS_MAP = {
        'list': CourseSerializer,
        'create': CreateCourseSerializer

    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(self.action, '')

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset
