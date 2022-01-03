from typing import List
from .base import BaseKeyboard
from apps.timetables.models import EducationalLevel
from vkbottle import Keyboard, Text


class EducationalLevelsKeyboard(BaseKeyboard):

    def __init__(self, levels: List[EducationalLevel]) -> None:
        super().__init__()
        self.levels = levels
        self.keyboard = self.init_keyboard()

    def init_keyboard(self) -> Keyboard:
        result = Keyboard()
        for index, value in enumerate(self.levels):
            result.add(Text(value.title))
            if not self._is_last(index):
                result.row()
        return result

    def to_api(self) -> str:
        return self.keyboard.get_json()

    def _is_last(self, index: int) -> bool:
        return index == len(self.levels) - 1
