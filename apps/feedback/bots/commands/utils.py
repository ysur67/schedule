from datetime import date, time
from functools import singledispatch
from time import strftime
from typing import Any, Dict, List
from apps.feedback.models import Profile
from apps.main.utils.date import get_day_of_week
from apps.timetables.models import Lesson
from apps.timetables.models.group import Group


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


def build_lessons_message(lessons_by_date: Dict[date, List[Lesson]], group: Group, date_start: date, date_end: date) -> str:
    result = f"Расписание {to_message_format(date_start)} - {to_message_format(date_end)}\n"
    result += f"Группа: {group.title}\n\n"
    for date in lessons_by_date:
        result += f"{get_day_of_week(date).capitalize()} {to_message_format(date)}\n"
        for index, lesson in enumerate(lessons_by_date[date]):
            result += f"{index + 1}. {lesson.subject.title}\n"
            result += f"\t🕐: {to_message_format(lesson.time_start)} - {to_message_format(lesson.time_end)}\n"
            result += f"\t👤: {lesson.teacher.name}\n"
            result += f"\t🏛: {lesson.classroom.title}\n"
            result += f"\tПрим.: {lesson.note}\n"
            result += "\n"
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
