from telebot import types


def lessons_keyboard(lessons):
    keyboard = types.InlineKeyboardMarkup()
    for lesson in lessons:
        text = f"""{lesson['date']}\t({lesson['time_start']} - {lesson['time_finish']})"""
        keyboard.add(
            types.InlineKeyboardButton(
                text=text,
                callback_data=f"lesson_{lesson['id']}",
            )
        )
    return keyboard
