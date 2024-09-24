from typing import Final


class CourseErrors:
    USER_IS_NOT_OPERATOR: Final[str] = 'Пользователь не является оператором'
    DATETIME_MUST_BE_IN_THE_FUTURE: Final[str] = 'Дата и время должны быть больше текущего времени'
