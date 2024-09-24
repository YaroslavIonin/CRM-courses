import datetime

from django.utils.timezone import make_aware

from rest_framework import serializers

from apps.courses.models import Course
from apps.courses.constants import CourseErrors
from apps.users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Course
        fields = '__all__'

    def validate_created_by(self, created_by):
        if not created_by.is_operator:
            raise serializers.ValidationError(
                CourseErrors.USER_IS_NOT_OPERATOR
            )
        return created_by


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'price',
            'date_time',
            'description',
        ]

    def create(self, validated_data: dict) -> Course:
        user = self.context['request'].user
        if not user.is_operator:
            raise serializers.ValidationError(
                {'user': CourseErrors.USER_IS_NOT_OPERATOR}
            )
        validated_data['created_by'] = user
        return super().create(validated_data)

    def validate_date_time(self, date_time):
        if date_time < make_aware(datetime.datetime.now()):
            raise serializers.ValidationError(
                CourseErrors.DATETIME_MUST_BE_IN_THE_FUTURE
            )

        return date_time

    @property
    def data(self):
        return CourseSerializer(
            instance=self.instance
        ).data


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'price',
            'date_time',
            'description',
        ]

    @property
    def data(self):
        return CourseSerializer(
            instance=self.instance
        ).data
