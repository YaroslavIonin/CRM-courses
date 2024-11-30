from telebot import types

from constants import EnrollmentButtonText, get_enrollment_text_new


def agreement_enrollment_keyboard(lesson_id):
    keyboard = types.InlineKeyboardMarkup(
        row_width=2,
    )
    agreement = types.InlineKeyboardButton(
        text=EnrollmentButtonText.AGREEMENT,
        callback_data=f"agreement_{lesson_id}"
    )
    disagreement = types.InlineKeyboardButton(
        text=EnrollmentButtonText.DISAGREEMENT,
        callback_data=f"disagreement_{lesson_id}",
    )
    keyboard.add(disagreement, agreement)
    return keyboard


def cancel_enrollment_keyboard(enrollment_id):
    keyboard = types.InlineKeyboardMarkup()
    cancel = types.InlineKeyboardButton(
        text=EnrollmentButtonText.DELETE_ENROLLMENT,
        callback_data=f"cancel_{enrollment_id}",
    )
    keyboard.add(cancel)
    return keyboard


def enrollments_keyboard(enrollments):
    keyboard = types.InlineKeyboardMarkup(
        row_width=5,
    )
    for enrollment in enrollments:
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{get_enrollment_text_new(enrollment)}",
                callback_data=f"enrollment_{enrollment['id']}",
            )
        )
    return keyboard
