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
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    logging.info(f"""
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
        'message': response.text
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
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    logging.info(f"""
    Sending request to {response.url}
    Response: {response.text}
    """)
    if response.status_code == 200:
        return {
            'status': 'success',
            'course': response.json(),
        }
    return {
        'status': 'error',
        'message': response.text
    }
