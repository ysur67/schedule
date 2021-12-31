from datetime import date, datetime
from typing import List, Optional
from apps.exchange.parse.utils import get_date_from_string, get_time_range_from_string
from apps.timetables.models.classroom import Classroom
from apps.timetables.models.group import Group
from apps.timetables.models.subject import Subject
from apps.timetables.models.teacher import Teacher
from apps.timetables.usecases.classroom import create_classroom, get_classroom_by_name

from apps.timetables.usecases.group import create_group, get_group_by_title
from apps.timetables.usecases.lesson import GetLessonParams, create_lesson, get_lesson_by_query_params
from apps.timetables.usecases.subject import create_subject, get_subject_by_title
from apps.timetables.usecases.teacher import create_teacher, get_teacher_by_name
from .base import BaseHttpParser
from bs4 import BeautifulSoup
from apps.timetables.models import Lesson


class MainSiteParser(BaseHttpParser):
    logging_name: str = "Main Site Parser"

    def on_set_up(self):
        super().on_set_up()
        self.logger.info("Начинается парсинг занятий...")
        self.logger.info("Полученный адрес: %s", self.url)
        self.logger.info("Поля запроса: %s", self.payload_data)

    def parse(self):
        date_titles = self.soup.find_all("h4")
        for title in date_titles:
            title: BeautifulSoup
            parent_center = title.parent
            current_date = get_date_from_string(title.get_text())
            table = parent_center.next_sibling
            if table.name != "table":
                self.logger.error("Не была найдена таблица")
                continue
            self.parse_table(table, current_date)

    def parse_table(self, table: BeautifulSoup, current_date: date) -> None:
        rows = table.find_all("tr")
        if not rows:
            return self.logger.error("Таблица не содержит строк!")
        # Удаляем первую строку из таблицы - это хедер
        rows.pop(0)
        _ = self.get_lesssons_from_rows(rows, current_date)

    def get_lesssons_from_rows(self, rows: BeautifulSoup, current_date: date) -> List[Lesson]:
        result = []
        for row in rows:
            lesson = self.get_lesson_from_single_row(row, current_date)
            if lesson:
                result.append(lesson)
        return result

    def get_lesson_from_single_row(self, row: BeautifulSoup, current_date: date) -> Optional[Lesson]:
        tds = row.find_all("td")
        if not tds:
            return self.logger.error("Строка не содержит значений, пропуск...")
        # Удаляем первый элемент - это номер строки
        tds.pop(0)
        # TODO: Вот с этим уродском, если возможно - что-то придумать
        for index, cell in enumerate(tds):
            if index == 0:
                group = self.parse_group(cell)
            elif index == 1:
                time_start, time_end = get_time_range_from_string(cell.get_text())
            elif index == 2:
                classroom = self.parse_classroom(cell)
            elif index == 3:
                subject = self.parse_subject(cell)
            elif index == 4:
                teacher = self.parse_teacher(cell)
            elif index == 5:
                note = self.parse_note(cell)
        lesson = get_lesson_by_query_params(GetLessonParams(
            group=group,
            time_start=time_start,
            classroom=classroom,
            lesson_date=current_date,
            subject=subject,
            teacher=teacher,
        ))
        if lesson:
            return lesson
        return create_lesson(
            title=subject.title,
            date=current_date,
            time_start=time_start,
            time_end=time_end,
            group=group,
            teacher=teacher,
            note=note,
            subject=subject,
            classroom=classroom
        )

    def parse_group(self, group: BeautifulSoup) -> Group:
        title = self._get_title(group)
        result = get_group_by_title(title)
        if result:
            return result
        return create_group(title=title)

    def parse_classroom(self, classroom: BeautifulSoup) -> Classroom:
        title = self._get_title(classroom)
        result = get_classroom_by_name(title)
        if result:
            return result
        return create_classroom(title=title)

    def parse_subject(self, subject: BeautifulSoup) -> Subject:
        title = self._get_title(subject)
        result = get_subject_by_title(title)
        if result:
            return result
        return create_subject(title=title)

    def parse_teacher(self, teacher: BeautifulSoup) -> Teacher:
        title = self._get_title(teacher)
        result = get_teacher_by_name(title)
        if result:
            return result
        return create_teacher(name=title)

    def parse_note(self, note: BeautifulSoup) -> Optional[str]:
        return self._get_title(note, raise_exception=False)

    def _get_title(self, item: BeautifulSoup, raise_exception: bool = True) -> Optional[str]:
        result = item.get_text()
        if result:
            return result
        if raise_exception:
            raise ValueError("bs item has no title inside it")
        return None
