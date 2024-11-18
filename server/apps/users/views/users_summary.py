from rest_framework import generics

from apps.users.models import User
from apps.users.serializers import UserSerializer
from django_filters import rest_framework as filters


class UserFilterSet(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'phone_number': ['icontains']
        }


class UserSummaryListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilterSet
