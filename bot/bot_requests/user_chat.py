import logging

import requests


def get_or_create_user_chat(base_domain, token, chat_id):
    """
    Gets or creates a user chat.
    """
    if not token:
        return {
            'status': 'error',
            'message': 'Token is required'
        }

    url = base_domain + "/users/chat/" + str(chat_id)
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(f"""
    Gets or creates a user chat.
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            "status": "success"
        }
    return {
        "status": "error",
    }
