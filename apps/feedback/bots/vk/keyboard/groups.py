from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from apps.timetables.usecases.group import get_groups_by_educational_level
from .base import BaseKeyboard
from apps.timetables.models import EducationalLevel
from vkbottle import Keyboard, Text


class GroupsKeyboard(BaseKeyboard):

    def __init__(self, level: EducationalLevel) -> None:
        super().__init__()
        self.level = level
        self.groups = get_groups_by_educational_level(self.level)
        self.keyboard = self.init_keyboard()

    def init_keyboard(self) -> None:
        result = Keyboard()
        for index, value in enumerate(self.groups):
            result.add(Text(value.title))
            if not self._is_last(index) and index % 2 == 0:
                result.row()
        return result

    def to_api(self) -> str:
        return self.keyboard.get_json()

    def _is_last(self, index: int) -> bool:
        return index == len(self.groups) - 1

