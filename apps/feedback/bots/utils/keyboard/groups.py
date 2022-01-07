from typing import Any, Iterable

from vkbottle.api import request_rescheduler
from vkbottle.tools.dev.keyboard.color import KeyboardButtonColor
from .base import BaseKeyboard
from vkbottle import Keyboard, Text
from apps.timetables.models import Group


class GroupsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> str:
        result = Keyboard()
        self.data: Iterable[Group]
        OFFSET = 3
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if (index + 1) % OFFSET == 0 and not self._is_last(index):
                result.row()
        result.row()
        result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()
