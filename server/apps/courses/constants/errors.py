from typing import Final


class CourseErrors:
    USER_IS_NOT_OPERATOR: Final[str] = 'Пользователь не является оператором'
    DATETIME_MUST_BE_IN_THE_FUTURE: Final[str] = 'Дата и время должны быть больше текущего времени'


class EnrollmentErrors:
    COURSE_NOT_IN_OPERATORS_COURSES: Final[str] = 'Оператор может записать пользователя только на свои курсы'
    OPERATOR_CANNOT_ENROLL_FOR_COURSE: Final[str] = 'Оператор не может записываться на курс'
    MAX_COUNT_ENROLLMENT_REACHED: Final[str] = 'Достигнуто максимальное количество записей на урок'
    LESSON_ALREADY_ENROLLED: Final[str] = 'Ученик уже записан на этот урок'
