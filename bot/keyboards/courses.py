from telebot import types


def courses_keyboard(courses):
    keyboard = types.InlineKeyboardMarkup()
    for course in courses:
        keyboard.add(
            types.InlineKeyboardButton(
                text=course['title'],
                callback_data=f"course_{course['id']}",
            )
        )
    return keyboard
