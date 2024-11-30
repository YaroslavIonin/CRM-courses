import logging

import requests


def get_user_summary(base_domain, phone_number):
    """
    Gets list summary of users
    """
    url = f"{base_domain}/users/summary"
    response = requests.get(
        url=url,
        params={
            "phone_number__icontains": phone_number,
        },
    )

    logging.info(
        f"""
    Gets list summary of users
    
    Sending request to {response.url}
    Response: {response.json()}
    """
    )

    if response.status_code == 200:
        users = response.json()

        if len(users) != 1:
            return {
                "status": "error",
                "message": "Пользователь не определен\nЗарегистрируйтесь в сервисе",
            }

        user = users[0]
        return {"status": "success", "user": user}

    return {"status": "error", "message": "Ошибка при проверке номера телефона."}
