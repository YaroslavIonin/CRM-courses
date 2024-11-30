from django.urls import path
from apps.users.views import UserSummaryListAPIView, UserChatRetrieveAPIView

urlpatterns = [
    path('summary', UserSummaryListAPIView.as_view()),
    path('chat/<str:chat_id>', UserChatRetrieveAPIView.as_view()),
]
