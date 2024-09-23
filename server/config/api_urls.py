from django.urls import path, include
from apps.courses.routers import courses_router

urlpatterns = [
    path('auth/', include('apps.users.urls.auth')),
] + courses_router.urls
