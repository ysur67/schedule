from typing import List
from .base import BaseKeyboard
from apps.timetables.models import EducationalLevel
from vkbottle import Keyboard, Text


class EducationalLevelsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> str:
        result = Keyboard()
        self.data: List[EducationalLevel]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index, self.data):
                result.row()
        return result.get_json()
