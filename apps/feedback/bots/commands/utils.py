from apps.feedback.models import Profile
from apps.timetables.models import Lesson


def build_status_message(profile: Profile) -> str:
    group = profile.get_group()
    result = f"Группа: {group.title}\n"
    result += f"Уровень образования: {group.level.title.capitalize()}\n"
    send_notifications = "✅ Включены" if profile.send_notifications else "❌ Отключены"
    result += f"Уведомления: {send_notifications}\n"
    for account in profile.get_accounts_in_messengers():
        messenger = account.get_messenger()
        result += f"Имеется аккаунт в {messenger.title}\n"
    return result


def build_lesson_message(lesson: Lesson) -> str:
    result = f"Дисциплина: {lesson.subject.title}\n"
    result += f"Дата: {lesson.date}\n"
    result += f"Время: {lesson.time_start} - {lesson.time_end}\n"
    result += f"Преподаватель: {lesson.teacher.name}\n"
    result += f"Аудитория: {lesson.classroom.title}\n"
    result += f"Примечание: {lesson.note}\n"
    return result
