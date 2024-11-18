from telebot import types


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=2,
    )
    all_courses = types.KeyboardButton("Все курсы", )
    my_enrollments = types.KeyboardButton("Мои записи")
    keyboard.add(all_courses, my_enrollments)
    return keyboard
