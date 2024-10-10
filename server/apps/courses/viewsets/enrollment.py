from typing import Type

from rest_framework import viewsets, serializers

from apps.courses.models import Course, Enrollment
from apps.courses.serializers import CreateEnrollmentSerializer, EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):

    SERIALIZER_CLASS_MAP = {
        'create': CreateEnrollmentSerializer,
        'list': EnrollmentSerializer,
    }

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        return self.SERIALIZER_CLASS_MAP.get(self.action, EnrollmentSerializer)

    def get_queryset(self) -> Type[list[Enrollment]]:
        if self.request.user.is_operator:
            return Enrollment.objects.filter(
                lesson__course__in=Course.objects.filter(
                    author=self.request.user,
                ))

        return Enrollment.objects.filter(
            user=self.request.user,
        )
