import logging

import requests


def get_token(base_domain, user, password):
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

    if response.status_code == 200:
        logging.info(f"""
        Sending request to {response.url}
        Response: {response.text}
        """)
        return {
            "status": "success",
            "message": f"Вы успешно вошли, {user['username']} ({user['phone_number']})!",
            "token": response.json()['access'],
        }
    return {
            "status": "error",
            "message": f"Ошибка авторизации. Проверьте ваши данные.",
        }
