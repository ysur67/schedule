from datetime import date
from typing import Any, Dict, Iterable, List

from apps.feedback.models import Profile
from apps.main.utils.date import get_day_of_week, to_message_format
from apps.timetables.models import Lesson
from apps.timetables.models.group import Group


def build_status_message(profile: Profile) -> str:
    group = profile.current_group
    result = ""
    if group:
        result += f"Группа: {group.title}\n"
        result += f"Уровень образования: {group.level.title.capitalize()}\n"
    else:
        result += "Группа: Не выбрана😥\n"
    result += "\n"
    send_notifications = "✅ Включены" if profile.send_notifications else "❌ Отключены"
    result += f"Уведомления о занятиях: {send_notifications}\n"
    result += "\n"
    result += f"Сейчас ты получаешь расписание на {profile.days_offset} дней вперед\n"
    result += "\n"
    for account in profile.get_accounts_in_messengers():
        messenger = account.get_messenger()
        result += f"Имеется аккаунт в {messenger.title}\n"
    return result


def build_lessons_message(
    lessons_by_date: Dict[date, List[Lesson]],
    group: Group,
    date_start: date,
    date_end: date = None
) -> List[str]:
    result: 'list[str]' = []
    for index, date_ in enumerate(lessons_by_date.keys()):
        message = build_lessons_message_by_date(date_, lessons_by_date[date_])
        if index == 0:
            message = build_lessons_message_title(
                group, date_start, date_end
            ) + message
        result.append(message)
    return result


def build_lessons_message_by_date(date_: date, lessons: Iterable[Lesson]) -> str:
    result = ''
    result += f"{get_day_of_week(date_).capitalize()} {to_message_format(date_)}\n\n"
    for index, lesson in enumerate(lessons):
        result += f"{index + 1}. {lesson.subject.title}\n"
        result += f"\t🕐 {to_message_format(lesson.time_start)} - {to_message_format(lesson.time_end)}\n"
        result += f"\t👤 {lesson.teacher.name}\n"
        if lesson.classroom:
            result += f"\t🏛 {lesson.classroom.title}\n"
        if lesson.href:
            result += f"\tСсылка: {lesson.href}\n"
        if lesson.note:
            result += f"\tПримечание: {lesson.note}\n"
    return result


def build_lessons_message_title(group: Group, date_start: date, date_end: date) -> str:
    result = ''
    result = f"Расписание {to_message_format(date_start)}"
    if date_end is not None:
        result += f" - {to_message_format(date_end)}"
    result += "\n"
    result += f"Группа: {group.title}\n\n"
    return result


def get_note_message() -> str:
    note_message = "Привет!\n"
    note_message += "Ты попросил отправлять тебе уведомления о занятиях "
    note_message += "в день их проведения.\n"
    note_message += "Поэтому, ниже отправляю тебе твои занятия на сегодня.\n"
    note_message += "Ты всегда можешь отключить уведомления в настройках"
    return note_message
