from django.urls import path
from ..views import UserSummaryListAPIView

urlpatterns = [
    path('summary', UserSummaryListAPIView.as_view()),
]
