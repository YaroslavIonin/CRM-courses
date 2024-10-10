from rest_framework import serializers

from apps.courses.models import Course
from apps.courses.constants import CourseErrors
from apps.users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Course
        fields = '__all__'

    def validate_author(self, author):
        if not author.is_operator:
            raise serializers.ValidationError(
                CourseErrors.USER_IS_NOT_OPERATOR
            )
        return author


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'price',
            'description',
        ]

    def create(self, validated_data: dict) -> Course:
        user = self.context['request'].user
        if not user.is_operator:
            raise serializers.ValidationError(
                {'user': CourseErrors.USER_IS_NOT_OPERATOR}
            )
        validated_data['author'] = user
        return super().create(validated_data)

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
            'description',
        ]

    @property
    def data(self):
        return CourseSerializer(
            instance=self.instance
        ).data
