from rest_framework import serializers

from .lesson import LessonSerializer
from ..models import Enrollment, Course
from ...users.serializers import UserSerializer
from ..constants.errors import EnrollmentErrors


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'user',
            'lesson',
        ]


class CreateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'lesson',
        ]

    def create(self, validated_data: dict) -> Course:
        user = self.context['request'].user
        if user.is_operator:
            raise serializers.ValidationError({
                "error": EnrollmentErrors.OPERATOR_CANNOT_ENROLL_FOR_COURSE,
            })

        validated_data['user'] = user
        return super().create(validated_data)

    def validate_lesson(self, lesson):
        user = self.context['request'].user
        try:
            Enrollment.objects.get(
                user=user,
                lesson=lesson
            )
        except Enrollment.DoesNotExist:
            if not lesson.is_available():
                raise serializers.ValidationError(
                    EnrollmentErrors.MAX_COUNT_ENROLLMENT_REACHED
                )
            return lesson
        raise serializers.ValidationError(
            EnrollmentErrors.LESSON_ALREADY_ENROLLED
        )

    @property
    def data(self):
        return EnrollmentSerializer(
            instance=self.instance
        ).data
