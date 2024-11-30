import dataclasses


def get_enrollment_text(enrollment):
    return (
        f"{enrollment['lesson']['course']['title']}\n"
        f"{enrollment['lesson']['date']}\n"
        f"({enrollment['lesson']['time_start']} - {enrollment['lesson']['time_finish']})"
    )


@dataclasses.dataclass
class EnrollmentButtonText:
    AGREEMENT = "Подтвердить запись"
    DISAGREEMENT = "Назад"

    DELETE_ENROLLMENT = "Отменить запись"


@dataclasses.dataclass
class AuthButtonText:
    SEND_CONTACT = "Отправить контакт"

    REGISTER = "Зарегистрироваться"


@dataclasses.dataclass
class MainButtonText:
    ALL_COURSES = "Все курсы"
    MY_ENROLLMENTS = "Мои записи"
