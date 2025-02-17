from django.urls import path, include
from apps.courses.routers import courses_router, enrollment_router, lesson_router

urlpatterns = [
    path('auth/', include('apps.users.urls.auth')),
    path('users/', include('apps.users.urls.users_summary')),
]

urlpatterns += courses_router.urls
urlpatterns += enrollment_router.urls
urlpatterns += lesson_router.urls
