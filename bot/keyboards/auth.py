from telebot import types

from bot.constants import AuthButtonText


def phone_keyboard(is_one_time=True):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=is_one_time,
        resize_keyboard=True,
    )
    markup.add(
        types.KeyboardButton(
            AuthButtonText.SEND_CONTACT,
            request_contact=True,
        ),
    )
    return markup


def register_keyboard(phone_number):
    keyboard = types.InlineKeyboardMarkup(
    )
    keyboard.add(
        types.InlineKeyboardButton(
            AuthButtonText.REGISTER,
            callback_data=f'register_{phone_number}',
        )
    )
    return keyboard


def use_tg_name_keyboard(username, full_name, phone_number):
    markup = types.InlineKeyboardMarkup(
    )
    markup.add(
        types.InlineKeyboardButton(
            text=username,
            callback_data=f"name_{username.replace('_', ' ')}_{phone_number}",
        ),
        types.InlineKeyboardButton(
            text=full_name,
            callback_data=f"name_{full_name.replace('_', ' ')}_{phone_number}",
        ),
    )
    return markup
