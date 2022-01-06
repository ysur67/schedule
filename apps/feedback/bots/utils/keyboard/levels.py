from typing import List
from .base import BaseKeyboard
from apps.timetables.models import EducationalLevel
from vkbottle import Keyboard, Text


class EducationalLevelsKeyboard(BaseKeyboard):

    def init_keyboard(self) -> Keyboard:
        result = Keyboard()
        self.data: List[EducationalLevel]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index):
                result.row()
        self.result = result
        return result

    def to_api(self) -> str:
        return self.keyboard.get_json()
