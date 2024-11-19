from telebot import types


def back_keyboard(call):
    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=call,
        )
    )
    return keyboard
