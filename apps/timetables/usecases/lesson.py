from typing import Any, Optional
from datetime import time, date
from apps.timetables.models import Lesson
from apps.timetables.models.classroom import Classroom
from apps.timetables.models.group import Group
from apps.timetables.models.subject import Subject
from apps.timetables.models.teacher import Teacher
from functools import singledispatch


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
