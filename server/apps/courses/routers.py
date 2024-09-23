from rest_framework.routers import DefaultRouter

from .viewsets import CourseViewSet


courses_router = DefaultRouter()
courses_router.register(
    r'courses',
    CourseViewSet,
    basename='courses'
)
