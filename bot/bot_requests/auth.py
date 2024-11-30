import logging

import requests


def get_token(base_domain, user, password):
    """
    Gets jwt token
    """
    logging.info(f"""
    User phone_number: {user['phone_number']}
    User password: {password}
    """)

    # Отправляем запрос на сервер для получения JWT токена
    response = requests.post(
        f"{base_domain}/auth/token/",
        json={
            "phone_number": user['phone_number'],
            "password": password
        }
    )
    logging.info(f"""
    Gets jwt token.
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            "status": "success",
            "message": f"Вы успешно вошли, {user['username']} ({user['phone_number']})!",
            "token": response.json()['access'],
        }
    return {
        "status": "error",
        "message": f"Ошибка авторизации. Проверьте ваши данные.",
    }


def create_user(base_domain, username, phone_number, password):
    logging.info(f"""
    User username: {username}
    User phone_number: {phone_number}
    User password: {password}
    """)

    # Отправляем запрос на сервер для получения JWT токена
    response = requests.post(
        f"{base_domain}/auth/register/",
        json={
            "username": username,
            "phone_number": f'+{phone_number}',
            "password": password,
        }
    )

    if response.status_code == 201:
        logging.info(f"""
            Sending request to {response.url}
            Response: {response.text}
            """)
        return {
            "status": "success",
            "message": f"{username}, вы зарегистрированы!",
            "user": response.json(),
        }
    return {
        "status": "error",
        "message": f"Не получилось зарегистрироваться\n{response.text}",
    }
