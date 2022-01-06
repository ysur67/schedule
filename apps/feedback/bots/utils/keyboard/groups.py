from typing import Any, Iterable
from .base import BaseKeyboard
from vkbottle import Keyboard, Text
from apps.timetables.models import Group


class GroupsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> str:
        result = Keyboard()
        self.data: Iterable[Group]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index):
                result.row()
        return result.get_json()
