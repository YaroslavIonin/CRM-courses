import os

from config.celery import app


@app.task()
def send_notify(chat_id, text_message, enrollment_id):
    from telebot import TeleBot, types

    bot = TeleBot(os.environ.get('TELEGRAM_TOKEN'))

    keyboard = types.InlineKeyboardMarkup(
        row_width=2,
    )
    agreement = types.InlineKeyboardButton(
        text="Отменить запись",
        callback_data=f"cancel_{enrollment_id}"
    )
    keyboard.add(agreement)

    bot.send_message(
        chat_id=chat_id,
        text=text_message,
        reply_markup=keyboard,
    )
