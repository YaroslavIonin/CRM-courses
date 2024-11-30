from telebot import types

from constants import MainButtonText


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
    )
    all_courses = types.KeyboardButton(text=MainButtonText.ALL_COURSES)
    my_enrollments = types.KeyboardButton(text=MainButtonText.MY_ENROLLMENTS)
    keyboard.add(all_courses, my_enrollments)
    return keyboard
