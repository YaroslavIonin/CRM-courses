def get_enrollment_text(enrollment):
    return f"{enrollment['lesson']['course']['title']}\n" \
           f"{enrollment['lesson']['date']}\n" \
           f"({enrollment['lesson']['time_start']} - {enrollment['lesson']['time_finish']})"


class EnrollmentButtonText:
    AGREEMENT = "Подтвердить запись"
    DISAGREEMENT = "Назад"

    DELETE_ENROLLMENT = "Отменить запись"
