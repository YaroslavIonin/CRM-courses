import logging

import requests


def get_lessons(base_domain, token, course_id):
    """
    Get lessons for a course
    """
    if not token:
        return {
            'status': 'error',
            'message': 'Token is required'
        }

    url = base_domain + f'/lessons'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.get(
        url=url,
        headers=headers,
        params={
            'course': course_id
        }
    )

    logging.info(f"""
    Get lessons for a course
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            'status': 'success',
            'lessons': response.json(),
        }
    return {
        'status': 'error',
        'message': response.text
    }


def get_lesson_by_id(base_domain, token, lesson_id):
    """
    Get lesson by id
    """
    if not token:
        return {
            'status': 'error',
            'message': 'Token is required'
        }

    url = base_domain + f'/lessons/{lesson_id}'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(f"""
    Get lesson by id
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            'status': 'success',
            'lesson': response.json(),
        }
    return {
        'status': 'error',
        'message': response.text
    }
