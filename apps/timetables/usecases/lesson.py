from typing import Optional
from datetime import time, date
from apps.timetables.models import Lesson
from apps.timetables.models.classroom import Classroom
from apps.timetables.models.group import Group
from apps.timetables.models.subject import Subject
from apps.timetables.models.teacher import Teacher


class GetLessonParams:

    def __init__(
        self,
        lesson_date: date,
        time_start: time,
        group: Group,
        classroom: Classroom,
        subject: Subject,
        teacher: Teacher
    ) -> None:
        self.date = lesson_date
        self.time_start = time_start
        self.group = group
        self.classroom = classroom
        self.subject = subject
        self.teacher = teacher


def get_lesson_by_query_params(param: GetLessonParams) -> Optional[Lesson]:
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
