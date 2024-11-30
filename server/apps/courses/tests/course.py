from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User

from apps.courses.models import Course, Lesson, Enrollment


class CourseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+79193654140", username="test", password="123"
        )
        self.operator = User.objects.create_user(
            phone_number="+79193654141",
            username="operator",
            is_operator=True,
            password="123",
        )

        self.user_token = RefreshToken.for_user(self.user).access_token
        self.operator_token = RefreshToken.for_user(self.operator).access_token

        self.user_client = APIClient()
        self.operator_client = APIClient()

        self.user_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        self.operator_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.operator_token}"
        )

        self.courses_url = "http://localhost:8000/api/v1/courses/"
        self.lessons_url = "http://localhost:8000/api/v1/lessons/"
        self.enrollments_url = "http://localhost:8000/api/v1/enrollments/"

        self.course = {
            "title": "Test Course",
            "description": "Test Course Description",
            "price": "100",
        }
        self.lesson = {
            "date": "2024-12-01",
            "time_start": "10:00:00",
            "time_finish": "11:00:00",
            "max_count_enrollments": 1,
        }

    def test_operator_create_course(self):
        course_before_count = Course.objects.filter(author=self.operator).count()

        response = self.operator_client.post(self.courses_url, data=self.course)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        courses = Course.objects.filter(author=self.operator)
        self.assertEqual(courses.count(), course_before_count + 1)

        course = courses.get()
        self.assertEqual(course.title, self.course["title"])

    def test_error_user_create_course(self):
        course_before_count = Course.objects.filter(author=self.user).count()

        response = self.user_client.post(self.courses_url, data=self.course)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        courses = Course.objects.filter(author=self.operator)
        self.assertEqual(courses.count(), course_before_count)

        self.assertEqual(response.data, {"user": "Пользователь не является оператором"})

    def test_operator_create_lesson(self):
        course = Course.objects.create(
            title=self.course["title"],
            description=self.course["description"],
            price=self.course["price"],
        )

        lesson_before_count = Lesson.objects.filter(
            course=course,
        ).count()
        self.lesson["course"] = course.id

        response = self.operator_client.post(self.lessons_url, data=self.lesson)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lessons = Lesson.objects.filter(course=course)
        self.assertEqual(lessons.count(), lesson_before_count + 1)

        lesson = lessons.get()
        self.assertEqual(lesson.course, course)
        self.assertEqual(
            str(lesson.date),
            self.lesson["date"],
        )

    def test_error_operator_create_enrollment(self):
        course = Course.objects.create(
            title=self.course["title"],
            description=self.course["description"],
            price=self.course["price"],
        )
        lesson = Lesson.objects.create(
            date=self.lesson["date"],
            time_start=self.lesson["time_start"],
            time_finish=self.lesson["time_finish"],
            max_count_enrollments=self.lesson["max_count_enrollments"],
            course=course,
        )

        self.enrollment = {
            "lesson": lesson.id,
        }
        enrollment_before_count = Enrollment.objects.filter(user=self.user).count()

        response = self.operator_client.post(self.enrollments_url, data=self.enrollment)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        enrollments = Enrollment.objects.filter(user=self.user)
        self.assertEqual(enrollments.count(), enrollment_before_count)

        self.assertEqual(
            response.data, {"error": "Оператор не может записываться на курс"}
        )
