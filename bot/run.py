import os
import logging

import telebot
from dotenv import load_dotenv

from bot.bot_requests import get_user_summary, get_token, get_all_courses, get_course, get_lessons, create_enrollment, \
    get_lesson_by_id
from bot.bot_requests.enrollments import get_all_enrollments
from bot.keyboards import phone_keyboard, main_keyboard, courses_keyboard, back_keyboard, agreement_enrollment, \
    enrollments_keyboard
from bot.keyboards.lessons import lessons_keyboard

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
        text="Привет! Я бот для записи на курсы\nПоделитесь своим контактом, чтобы авторизоваться в сервисе",
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
            else:
                bot.send_message(
                    message.chat.id,
                    "Курсы отсутствуют"
                )

    elif message.text == "Мои записи":
        response = get_all_enrollments(base_domain, user_data[message.chat.id])
        if response['status'] == "error":
            bot.send_message(message.chat.id, response['message'])
        else:
            enrollments = response['data']
            if len(enrollments) :
                bot.send_message(
                    message.chat.id,
                    "Ваши записи",
                    reply_markup=enrollments_keyboard(enrollments),
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "Нет записей"
                )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("course_")
)
def handle_course_click(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    course_id = call.data.split("_")[1]
    response = get_course(
        base_domain,
        user_data[call.from_user.id],
        course_id
    )
    if response['status'] == "error":
        bot.send_message(
            call.message.chat.id,
            response['message'],
        )
    else:
        title = response['course']['title']
        description = response['course']['description']
        price = response['course']['price']
        author = response['course']['author']['username']
        res_course = '\n'.join([
            title,
            description,
            f'\nЦена: {price}',
            f'Автор: {author}',
        ])
        bot.send_message(
            call.message.chat.id,
            res_course,
            reply_markup=back_keyboard("Все курсы")
        )
        get_lesson_handle(
            call.message,
            response['course']['id'],
        )


def get_lesson_handle(message, course_id):
    response = get_lessons(
        base_domain,
        user_data[message.chat.id],
        course_id
    )
    if response['status'] == "error":
        bot.send_message(
            message.chat.id,
            response['message'],
        )
    else:
        lessons = response['lessons']
        if lessons:
            keyboard = lessons_keyboard(lessons)
            bot.send_message(
                message.chat.id,
                'Выберите свободное время для записи',
                reply_markup=keyboard,
            )
        else:
            bot.send_message(
                message.chat.id,
                'Пока нет занятий этого курса.',
            )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("lesson_")
)
def handle_lesson_click(call):
    lesson_id = call.data.split("_")[1]
    response = get_lesson_by_id(
        base_domain,
        user_data[call.from_user.id],
        lesson_id
    )
    if response['status'] == "error":
        bot.send_message(
            call.message.chat.id,
            response['message'],
        )
    else:
        lesson = response['lesson']
        if not bool(lesson['is_available']):
            bot.send_message(
                call.message.chat.id,
                "Закончились свободные места. Выберите другое время.",
                reply_markup=back_keyboard("Все курсы")
            )
        else:
            text = f"""
Запись на курс: {lesson['course']['title']}
    Дата: {lesson['date']}
    Время: {lesson['time_start']} - {lesson['time_finish']}
    Стоимость: {lesson['course']['price']}
            
Вы хотите записаться на этот курс?
            """
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=agreement_enrollment(lesson['id'])
            )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("agreement_") or call.data.startswith('disagreement_')
)
def agreements_buttons_click(call):
    status, lesson_id = call.data.split("_")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if status == "agreement":
        response = create_enrollment(
            base_domain,
            user_data[call.message.chat.id],
            lesson_id
        )
        if response['status'] == "error":
            bot.send_message(
                call.message.chat.id,
                response['message'],
                reply_markup=main_keyboard()
            )
        else:
            # bot.delete_message(call.message.chat.id, call.message.message_id)
            # bot.delete_message(call.message.chat.id, call.message.message_id)

            enrollment = response['data']
            text = f"""
Вы записаны на курс: {enrollment['lesson']['course']['title']}
    Дата: {enrollment['lesson']['date']}
    Время: {enrollment['lesson']['time_start']} - {enrollment['lesson']['time_finish']}
    Стоимость: {enrollment['lesson']['course']['price']}
        
За два часа до начала занятия мы вас уведомим.
            """
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=main_keyboard()
            )


if __name__ == '__main__':
    bot.polling(none_stop=False)
