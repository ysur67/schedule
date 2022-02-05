from datetime import date, time, timedelta
from functools import singledispatch
from multiprocessing.sharedctypes import Value
from typing import Any, Dict, List, Optional

from django.db.models.query import QuerySet

from apps.feedback.const import DEFAULT_DAYS_OFFSET
from apps.feedback.models import Profile
from apps.main.utils.date import date_range
from apps.timetables.models import Lesson
from apps.timetables.models.classroom import Classroom
from apps.timetables.models.group import Group
from apps.timetables.models.subject import Subject
from apps.timetables.models.teacher import Teacher
from apps.timetables.usecases.group import get_groups_that_have_lessons_in_date


class GetLessonByDateAndClassroomParam:

    def __init__(
        self,
        lesson_date: date,
        time_start: time,
        group: Group,
        classroom: Classroom,
        teacher: Teacher
    ) -> None:
        self.date = lesson_date
        self.time_start = time_start
        self.group = group
        self.classroom = classroom
        self.teacher = teacher


class AllFieldsParam(GetLessonByDateAndClassroomParam):

    def __init__(
        self,
        lesson_date: date,
        time_start: time,
        group: Group,
        classroom: Classroom,
        teacher: Teacher,
        subject: Subject
    ) -> None:
        super().__init__(lesson_date, time_start, group, classroom, teacher)
        self.subject = subject


@singledispatch
def get_lesson_by_params(param: Any) -> Optional[Lesson]:
    raise NotImplementedError(f"there is no approach for type {type(param)}")


@get_lesson_by_params.register(GetLessonByDateAndClassroomParam)
def _(param: GetLessonByDateAndClassroomParam) -> Optional[Lesson]:
    return Lesson.objects.filter(
        date=param.date,
        time_start=param.time_start,
        group=param.group,
        classroom=param.classroom,
        teacher=param.teacher
    ).first()

@get_lesson_by_params.register(AllFieldsParam)
def _(param: AllFieldsParam) -> Optional[Lesson]:
    return Lesson.objects.filter(
        date=param.date,
        time_start=param.time_start,
        group=param.group,
        classroom=param.classroom,
        subject=param.subject,
        teacher=param.teacher
    ).first()


def create_lesson(**options) -> Lesson:
    return Lesson.objects.create(**options)


def get_lessons_by_date_and_group(date: date, group: Group) -> QuerySet[Lesson]:
    return Lesson.objects.filter(date=date, group=group)


def get_lessons_by_group_and_date_range(group: Group, start: date, end: date) -> QuerySet[Lesson]:
    return Lesson.objects.filter(date__range=[start, end], group=group)


def get_lessons_dict_by_group_and_date_range(group: Group, start: date, end: date = None) -> Dict[date, List[Lesson]]:
    """Получить `Dict`, вида `[date]: List[Lesson]`, который будет содержать
    только даты с занятиями.

    Args:
        group (Group): Группа, для которой надо сформировать ответ
        start (date): Дата начала
        end (date, optional): Дата конца, если не указана,
        то +`apps.feedback.const.DEFAULT_DAYS_OFFSET` дней от начала

    Returns:
        Dict[date, List[Lesson]]: Результат запроса
    """
    if end is not None:
        if start > end:
            raise ValueError("Дата начала не может быть меньше конечной даты")
    else:
        end = start + timedelta(days=DEFAULT_DAYS_OFFSET)
    result: Dict[date, List[Lesson]] = {}
    if not get_lessons_by_group_and_date_range(group, start, end):
        return {}
    for single_date in date_range(start, end):
        qs = get_lessons_by_date_and_group(single_date, group)
        if qs.exists():
            result.setdefault(single_date, [])
            result[single_date] = qs
    return result


def get_lessons_by_profile_and_date(profile: Profile, date_: date) -> QuerySet[Lesson]:
    return Lesson.objects.filter(group=profile.get_group(), date=date_)
