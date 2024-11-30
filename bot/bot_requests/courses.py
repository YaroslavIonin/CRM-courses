import logging

import requests


def get_all_courses(base_domain, token):
    """
    Get all courses
    """
    if not token:
        return {
            'status': 'error',
            'message': 'Token is required'
        }

    url = base_domain + '/courses'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(f"""
    Get all courses.
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            'status': 'success',
            'courses': response.json(),
        }
    return {
        'status': 'error',
        'message': response.text,
    }


def get_course(base_domain, token, course_id):
    """
    Get a course
    """
    if not token:
        return {
            'status': 'error',
            'message': 'Token is required'
        }

    url = base_domain + f'/courses/{course_id}'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(f"""
    Get a course
    
    Sending request to {response.url}
    Response: {response.text}
    """)

    if response.status_code == 200:
        return {
            'status': 'success',
            'course': {
                "id": response.json()['id'],
                "author": {
                    "id": response.json()['author']['id'],
                    "username": response.json()['author']['username'],
                    "phone_number": response.json()['author']['phone_number'],
                },
                "title": response.json()['title'],
                "price": response.json()['price'],
                "description": response.json()['description'],
            },
        }
    return {
        'status': 'error',
        'message': response.text
    }
