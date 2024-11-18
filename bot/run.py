import os
import logging

import telebot
from dotenv import load_dotenv

from bot.bot_requests import get_user_summary, get_token, get_all_courses, get_course
from bot.keyboards import phone_keyboard, main_keyboard, courses_keyboard

logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    filemode='w',
)

load_dotenv('../.env')

bot = telebot.TeleBot(os.environ.get('YOUR_BOT_TOKEN'))
base_domain = 'http://0.0.0.0:8000/api/v1'

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Я бот для записи на курсы???. Поделитесь своим контактом, чтобы авторизоваться в сервисе",
        reply_markup=phone_keyboard()
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_contact = message.contact
    logging.info(f'User phone_number: {user_contact.phone_number}')

    response = get_user_summary(base_domain, user_contact.phone_number)
    if response['status'] == 'error':
        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
            reply_markup=phone_keyboard()
        )
    else:
        user = response['user']
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Здравствуйте, {user['username']}! Введите пароль:",
        )
        bot.register_next_step_handler(
            message,
            handle_password,
            user
        )


def handle_password(message, user):
    password = message.text
    bot.delete_message(message.chat.id, message.message_id)

    # Отправляем запрос на сервер для получения JWT токена
    response = get_token(base_domain, user, password)
    if response['status'] == "error":
        bot.send_message(
            message.chat.id,
            response['message'],
        )
    else:
        bot.send_message(
            message.chat.id,
            response['message'],
            reply_markup=main_keyboard(),
        )
        user_data[message.chat.id] = response['token']


@bot.message_handler(
    func=lambda message: message.text in ["Все курсы", "Мои записи"]
)
def main_button_click(message):
    if message.text == "Все курсы":

        response = get_all_courses(base_domain, user_data[message.chat.id])
        if response['status'] == "error":
            bot.send_message(message.chat.id, response['message'])
        else:
            courses = response['courses']
            if courses:
                bot.send_message(
                    message.chat.id,
                    "Выберите курс",
                    reply_markup=courses_keyboard(courses),
                )
                bot.register_next_step_handler(
                    message,
                    handle_course_click,
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "Курсы отсутствуют"
                )

    elif message.text == "Мои записи":
        # Здесь выполните второй запрос
        bot.send_message(message.chat.id, "Вы выбрали Мои записи. Выполняется...")
        # Добавьте код для выполнения запроса


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("course_")
)
def handle_course_click(call):
    course_id = call.data.split("_")[1]
    response = get_course(base_domain, user_data[call.from_user.id], course_id)
    if response['status'] == "error":
        bot.send_message(
            call.message.chat.id,
            response['message'],
        )
    else:
        course = response['course']
        bot.send_message(
            call.message.chat.id,
            f"{course}"
        )


if __name__ == '__main__':
    bot.polling(none_stop=False)
