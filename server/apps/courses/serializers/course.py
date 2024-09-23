import datetime

from django.utils.timezone import make_aware

from rest_framework import serializers

from apps.courses.models import Course
from apps.users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Course
        fields = '__all__'


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
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def validate_date_time(self, date_time):
        if date_time < make_aware(datetime.datetime.now()):
            raise serializers.ValidationError('Дата и время должны быть больше текущего времени')
        return date_time
