from datetime import date, time
from functools import singledispatch
from typing import Any
from apps.feedback.models import Profile
from apps.main.utils.date import get_day_of_week
from apps.timetables.models import Lesson


def build_status_message(profile: Profile) -> str:
    group = profile.get_group()
    result = ""
    if group:
        result += f"Группа: {group.title}\n"
        result += f"Уровень образования: {group.level.title.capitalize()}\n"
    send_notifications = "✅ Включены" if profile.send_notifications else "❌ Отключены"
    result += f"Уведомления: {send_notifications}\n"
    for account in profile.get_accounts_in_messengers():
        messenger = account.get_messenger()
        result += f"Имеется аккаунт в {messenger.title}\n"
    return result


def build_lesson_message(lesson: Lesson) -> str:
    result = f"{get_day_of_week(lesson.date).upper()}\n"
    result += f"Дисциплина: {lesson.subject.title}\n"
    result += f"Дата: {to_message_format(lesson.date)}\n"
    result += f"Время: {to_message_format(lesson.time_start)} - {to_message_format(lesson.time_end)}\n"
    result += f"Преподаватель: {lesson.teacher.name}\n"
    result += f"Аудитория: {lesson.classroom.title}\n"
    result += f"Примечание: {lesson.note}\n"
    return result


@singledispatch
def to_message_format(data: Any) -> str:
    raise NotImplementedError(f"There is no approach for type {type(data)}")

@to_message_format.register(date)
def _(data: date) -> str:
    return data.strftime('%d.%m.%Y')

@to_message_format.register(time)
def _(data: time) -> str:
    return data.strftime("%H:%M")
