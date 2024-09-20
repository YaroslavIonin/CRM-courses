from rest_framework import serializers

from ..models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)
