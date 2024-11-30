from datetime import datetime, timedelta

from apps.users.models import UserChat

from apps.courses.tasks import send_notify


def planed_enrollment_notify(enrollment, user_id):
    lesson_datetime = datetime.combine(
        enrollment.lesson.date,
        enrollment.lesson.time_start,
    )
    notify_time = lesson_datetime - timedelta(hours=1)

    chat_id = UserChat.objects.get(
        user_id=user_id,
    ).chat_id
    text_message = f"""
    Напоминание о занятии!

    {enrollment.lesson.course.title}
    {enrollment.lesson.date}
    {enrollment.lesson.time_start} - {enrollment.lesson.time_finish}
    """

    if notify_time <= datetime.now():
        notify_time = datetime.now() + timedelta(minutes=1)

    send_notify.s(
        chat_id=chat_id,
        text_message=text_message,
        enrollment_id=enrollment.id,
    ).apply_async(
        eta=notify_time - timedelta(hours=5),
    )
