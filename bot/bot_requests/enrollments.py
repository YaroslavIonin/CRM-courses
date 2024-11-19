import logging

import requests


def create_enrollment(base_domain, token, lesson_id):
    """
    Creates an enrollment for the given lesson.
    """
    url = base_domain + "/enrollments/"
    data = {
        "lesson": lesson_id,
    }
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.post(
        url,
        data=data,
        headers=headers,
    )
    logging.info(f"""
    Sending request to {response.url}
    Response: {response.text}
    """)
    if response.status_code == 201:
        return {
            "status": "success",
            "data": response.json(),
        }

    return {
        "status": "error",
        "message": response.text,
    }


def get_all_enrollments(base_domain, token):
    """
    Gets all enrollments.
    """
    url = base_domain + "/enrollments"
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(
        url,
        headers=headers,
    )
    logging.info(f"""
    Sending request to {response.url}
    Response: {response.text}
    """)
    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
        }
    return {
        "status": "error",
        "message": response.text,
    }