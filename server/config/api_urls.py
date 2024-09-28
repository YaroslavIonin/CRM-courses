from django.urls import path, include
from apps.courses.routers import courses_router, enrollment_router

urlpatterns = [
    path('auth/', include('apps.users.urls.auth')),
]

urlpatterns += courses_router.urls
urlpatterns += enrollment_router.urls
