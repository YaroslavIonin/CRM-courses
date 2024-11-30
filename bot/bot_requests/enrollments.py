import logging

import requests


def create_enrollment(base_domain, token, lesson_id):
    """
    Creates an enrollment for the given lesson.
    """
    if not token:
        return {"status": "error", "message": "Token is required"}

    url = base_domain + "/enrollments/"
    data = {
        "lesson": lesson_id,
    }
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = requests.post(
        url=url,
        data=data,
        headers=headers,
    )

    logging.info(
        f"""
    Creates an enrollment for the given lesson.
    
    Sending request to {response.url}
    Response: {response.text}
    """
    )

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
    if not token:
        return {"status": "error", "message": "Token is required"}

    url = base_domain + "/enrollments"
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(
        f"""
    Gets all enrollments.
    
    Sending request to {response.url}
    Response: {response.text}
    """
    )

    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
        }
    return {
        "status": "error",
        "message": response.text,
    }


def get_enrollment_by_id(base_domain, token, enrollment_id):
    """
    Gets an enrollment by its ID.
    """
    if not token:
        return {"status": "error", "message": "Token is required"}

    url = base_domain + "/enrollments/" + enrollment_id
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(
        url=url,
        headers=headers,
    )

    logging.info(
        f"""
    Gets an enrollment by its ID.
    
    Sending request to {response.url}
    Response: {response.text}
    """
    )

    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
        }
    return {
        "status": "error",
        "message": response.text,
    }


def delete_enrollment_by_id(base_domain, token, enrollment_id):
    """
    Deletes an enrollment by its ID.
    """
    if not token:
        return {"status": "error", "message": "Token is required"}

    url = base_domain + "/enrollments/" + enrollment_id + "/"
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = requests.delete(
        url=url,
        headers=headers,
    )

    logging.info(
        f"""
    Deletes an enrollment by its ID.
     
    Sending request to {response.url}
    Response: {response.text}
    """
    )

    if response.status_code == 204:
        return {
            "status": "success",
            "message": "Вы отменили занятие",
        }
    return {
        "status": "error",
        "message": response.text,
    }
