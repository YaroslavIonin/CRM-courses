from rest_framework import serializers

from . import CourseSerializer
from ..models import Enrollment, Course
from ...users.serializers import UserSerializer
from ..constants.errors import EnrollmentErrors


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'user',
            'course',
        ]


class CreateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'user',
            'course',
        ]

    def validate_course(self, course):
        user = self.context['request'].user
        if user.is_operator:
            if course not in Course.objects.filter(
                created_by=user,
            ):
                raise serializers.ValidationError(
                    EnrollmentErrors.COURSE_NOT_IN_OPERATORS_COURSES
                )

        return course

    def validate_user(self, user_for_enroll):
        user = self.context['request'].user
        if user.is_operator:
            raise serializers.ValidationError(
                EnrollmentErrors.OPERATOR_CANNOT_ENROLL_FOR_COURSE
            )

        return user_for_enroll

    @property
    def data(self):
        return EnrollmentSerializer(
            instance=self.instance
        ).data
