import dataclasses


def input_password_text(username):
    return f"Здравствуйте, {username}! Введите пароль:"


def get_course_text(course):
    return f"""{course['title']}
    Описание: {course['description']}
    Цена: {course['price']}
    Автор: {course['author']['username']}
    """


def get_pre_enrollment_text(lesson):
    return f"""Запись на курс: {lesson['course']['title']}
    Дата: {lesson['date']}
    Время: {lesson['time_start']} - {lesson['time_finish']}
    Стоимость: {lesson['course']['price']}  
    Вы хотите записаться на этот курс?
    """


def get_new_enrollment_text(enrollment):
    return f"""Вы записаны на курс: {enrollment['lesson']['course']['title']}
    Дата: {enrollment['lesson']['date']}
    Время: {enrollment['lesson']['time_start']} - {enrollment['lesson']['time_finish']}
    Стоимость: {enrollment['lesson']['course']['price']}
    За час до начала занятия мы вас уведомим.
    """


def get_enrollment_text_new(enrollment):
    return f"""Запись на курс: {enrollment['lesson']['course']['title']}
    Дата: {enrollment['lesson']['date']}
    Время: {enrollment['lesson']['time_start']} - {enrollment['lesson']['time_finish']}
    Стоимость: {enrollment['lesson']['course']['price']}
    """


@dataclasses.dataclass
class TextConst:
    HELLO_CONTACT = (
        "Привет! Я бот для записи на курсы"
        "\nПоделитесь своим контактом, чтобы авторизоваться в сервисе"
    )

    GET_USERNAME = "Выберите никнейм"
    GET_PASSWORD = "Придумайте и введите пароль"

    SELECT_COURSE = "Выберите интересующий курс"
    NO_COURSES = "Пока нет доступных курсов"

    YOUR_ENROLLMENTS = "Ваши записи\nВы можете посмотреть или отменить их"
    NOT_ENROLLMENTS = "Пока нет записей. Выберите курс и запишитесь на занятие"

    SELECT_LESSON = "Выберите свободное время для записи"
    NO_LESSONS = "Пока нет занятий этого курса"

    PRE_ENROLLMENT = "Предварительная запись"
