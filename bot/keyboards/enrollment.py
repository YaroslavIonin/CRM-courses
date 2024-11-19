from telebot import types


def agreement_enrollment(lesson_id):
    keyboard = types.InlineKeyboardMarkup(
        row_width=2,
    )
    agreement = types.InlineKeyboardButton(
        text="Подтвердить запись",
        callback_data=f"agreement_{lesson_id}"
    )
    disagreement = types.InlineKeyboardButton(
        text="Отменить",
        callback_data=f"disagreement_{lesson_id}",
    )
    keyboard.add(disagreement, agreement)
    return keyboard


def enrollments_keyboard(enrollments):
    keyboard = types.InlineKeyboardMarkup(
        row_width=2,
    )
    for i, enrollment in enumerate(enrollments):
        keyboard.add(
            types.InlineKeyboardButton(
                text='Запись',
                callback_data=f"enrollment_{i}"
            )
        )
        return keyboard
