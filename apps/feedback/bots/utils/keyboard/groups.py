from typing import Any, Iterable
from .base import BaseKeyboard
from vkbottle import Keyboard, Text
from apps.timetables.models import Group


class GroupsKeyboard(BaseKeyboard):

    def __init__(self, initial: Any) -> None:
        super().__init__(initial)

    def init_keyboard(self) -> None:
        result = Keyboard()
        self.data: Iterable[Group]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index) and index % 2 == 0:
                result.row()
        self.result = result
        return result

    def to_api(self) -> str:
        return self.keyboard.get_json()
