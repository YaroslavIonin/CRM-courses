import os
import logging

import telebot
from dotenv import load_dotenv

from bot.bot_requests import (
    get_token,
    get_course,
    create_user,
    get_lessons,
    get_all_courses,
    get_lesson_by_id,
    get_user_summary,
    create_enrollment,
    get_all_enrollments,
    get_enrollment_by_id,
    delete_enrollment_by_id,
)
from bot.constants import (
    TextConst,
    get_course_text,
    get_enrollment_text,
    input_password_text,
    get_pre_enrollment_text,
    get_new_enrollment_text,
)
from bot.keyboards import (
    main_keyboard,
    phone_keyboard,
    lessons_keyboard,
    courses_keyboard,
    register_keyboard,
    enrollments_keyboard,
    use_tg_name_keyboard,
    cancel_enrollment_keyboard,
    agreement_enrollment_keyboard,
)

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
        text=TextConst.HELLO_CONTACT,
        reply_markup=phone_keyboard(False)
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    logging.info(f'User: {message.contact}')

    response = get_user_summary(base_domain, phone_number)
    if response['status'] == 'error':
        if response['message'].startswith('Пользователь не определен'):
            keyboard = register_keyboard(phone_number)
            text = response['message']
        else:
            keyboard = phone_keyboard(False)
            text = response['message']

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard,
        )
    else:
        user = response['user']
        user_data[message.chat.id] = user
        bot.send_message(
            chat_id=message.chat.id,
            text=input_password_text(user['username']),
        )
        bot.register_next_step_handler(
            message,
            handle_password,
            user
        )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("register_")
)
def first_step_register_handler(call):
    full_name = call.from_user.full_name
    username = call.from_user.username
    phone_number = call.data.split("_")[1]

    bot.delete_message(call.message.chat.id, call.message.message_id)

    bot.send_message(
        chat_id=call.message.chat.id,
        text=TextConst.GET_USERNAME,
        reply_markup=use_tg_name_keyboard(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
        )
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("name_")
)
def second_step_register_handler(call):
    username = call.data.split("_")[1]
    phone_number = call.data.split("_")[2]

    bot.delete_message(call.message.chat.id, call.message.message_id)

    bot.send_message(
        chat_id=call.message.chat.id,
        text=TextConst.GET_PASSWORD,
    )
    bot.register_next_step_handler(
        call.message,
        register,
        user_name=username,
        phone_number=phone_number,
    )


def register(message, user_name, phone_number):
    bot.delete_messages(
        message.chat.id,
        [message.message_id, message.message_id - 1]
    )
    response = create_user(
        base_domain,
        username=user_name,
        phone_number=phone_number,
        password=message.text
    )

    if response['status'] == "error":
        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
        )
    else:
        user = response['user']
        user_data[message.chat.id] = user

        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
            reply_markup=main_keyboard(),
        )
        get_token_response(message, user, message.text)


def handle_password(message, user):
    password = message.text
    bot.delete_message(message.chat.id, message.message_id)

    # Отправляем запрос на сервер для получения JWT токена
    get_token_response(message, user, password)


def get_token_response(message, user, password):
    response = get_token(base_domain, user, password)
    if response['status'] == "error":
        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
            reply_markup=main_keyboard(),
        )
        user_data[message.chat.id]['token'] = response['token']


@bot.message_handler(
    func=lambda message: message.text in ["Все курсы", "Мои записи"]
)
def main_button_click(message):
    if message.text == "Все курсы":

        response = get_all_courses(
            base_domain,
            user_data[message.chat.id]['token']
        )
        if response['status'] == "error":
            bot.send_message(
                chat_id=message.chat.id,
                text=response['message']
            )
        else:
            courses = response['courses']
            if courses:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=TextConst.SELECT_COURSE,
                    reply_markup=courses_keyboard(courses),
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=TextConst.NO_COURSES,
                )

    elif message.text == "Мои записи":
        response = get_all_enrollments(
            base_domain,
            user_data[message.chat.id]['token']
        )
        if response['status'] == "error":
            bot.send_message(message.chat.id, response['message'])
        else:
            enrollments = response['data']
            print(len(enrollments))
            if len(enrollments):
                bot.send_message(
                    chat_id=message.chat.id,
                    text=TextConst.YOUR_ENROLLMENTS,
                    reply_markup=enrollments_keyboard(enrollments),
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=TextConst.NOT_ENROLLMENTS,
                )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("course_")
)
def handle_course_click(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    course_id = call.data.split("_")[1]
    response = get_course(
        base_domain,
        user_data[call.from_user.id]['token'],
        course_id
    )
    if response['status'] == "error":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=response['message'],
        )
    else:
        bot.send_message(
            chat_id=call.message.chat.id,
            text=get_course_text(response['course']),
            reply_markup=main_keyboard()
        )
        get_lesson_handle(
            call.message,
            response['course']['id'],
        )


def get_lesson_handle(message, course_id):
    response = get_lessons(
        base_domain,
        user_data[message.chat.id]['token'],
        course_id
    )
    if response['status'] == "error":
        bot.send_message(
            chat_id=message.chat.id,
            text=response['message'],
        )
    else:
        lessons = response['lessons']
        if lessons:
            keyboard = lessons_keyboard(lessons)
            bot.send_message(
                chat_id=message.chat.id,
                text=TextConst.SELECT_LESSON,
                reply_markup=keyboard,
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=TextConst.NO_LESSONS,
            )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("lesson_")
)
def handle_lesson_click(call):
    lesson_id = call.data.split("_")[1]
    response = get_lesson_by_id(
        base_domain,
        user_data[call.from_user.id]['token'],
        lesson_id
    )
    if response['status'] == "error":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=response['message'],
        )
    else:
        lesson = response['lesson']
        bot.send_message(
            chat_id=call.message.chat.id,
            text=get_pre_enrollment_text(lesson),
            reply_markup=agreement_enrollment_keyboard(lesson['id'])
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
            user_data[call.message.chat.id]['token'],
            lesson_id
        )
        if response['status'] == "error":
            bot.send_message(
                chat_id=call.message.chat.id,
                text=response['message'],
                reply_markup=main_keyboard()
            )
        else:
            enrollment = response['data']
            bot.send_message(
                chat_id=call.message.chat.id,
                text=get_new_enrollment_text(enrollment),
                reply_markup=main_keyboard()
            )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("enrollment_")
)
def enrollments_buttons_click(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    enrollment_id = call.data.split("_")[1]
    response = get_enrollment_by_id(
        base_domain,
        user_data[call.message.chat.id]['token'],
        enrollment_id
    )
    if response['status'] == "error":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=response['message'],
            reply_markup=main_keyboard()
        )
    else:
        enrollment = response['data']
        bot.send_message(
            chat_id=call.message.chat.id,
            text=get_enrollment_text(enrollment),
            reply_markup=cancel_enrollment_keyboard(enrollment['id']),
        )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("cancel_")
)
def cancel_enrollment_handler(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    enrollment_id = call.data.split("_")[1]
    response = delete_enrollment_by_id(
        base_domain,
        user_data[call.message.chat.id]['token'],
        enrollment_id
    )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=response['message'],
        reply_markup=main_keyboard()
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
