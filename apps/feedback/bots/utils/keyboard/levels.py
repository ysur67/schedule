from typing import List

from django.db.models.query import QuerySet
from vkbottle import Keyboard, KeyboardButtonColor, Text

from apps.timetables.models import EducationalLevel

from .base import BaseKeyboard


class EducationalLevelsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> str:
        result = Keyboard()
        self.data: QuerySet[EducationalLevel]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index, self.data):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()
