from rest_framework.routers import DefaultRouter

from .viewsets import CourseViewSet, EnrollmentViewSet


courses_router = DefaultRouter()
enrollment_router = DefaultRouter()

courses_router.register(
    r'courses',
    CourseViewSet,
    basename='courses'
)

enrollment_router.register(
    r'enrollments',
    EnrollmentViewSet,
    basename='enrollments'
)
