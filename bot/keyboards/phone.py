from telebot import types


def phone_keyboard():
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
    )
    markup.add(
        types.KeyboardButton(
            'Отправить контакт',
            request_contact=True,
        ),
    )
    return markup
