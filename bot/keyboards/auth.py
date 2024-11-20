from telebot import types


def phone_keyboard(is_one_time=True):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=is_one_time,
        resize_keyboard=True,
    )
    markup.add(
        types.KeyboardButton(
            'Отправить контакт',
            request_contact=True,
        ),
    )
    return markup


def register_keyboard(phone_number):
    markup = types.InlineKeyboardMarkup(
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Зарегистрироваться',
            callback_data=f'register_{phone_number}',
        )
    )
    return markup

