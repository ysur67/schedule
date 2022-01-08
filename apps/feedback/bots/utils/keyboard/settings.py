from typing import Iterable, List, Union
from vkbottle import Keyboard, Text
from vkbottle.tools.dev.keyboard.color import KeyboardButtonColor
from .base import BaseKeyboard, Button


class SettingsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> Union[str, List[str]]:
        result = Keyboard(inline=self.is_inline)
        self.data: Iterable[Button]
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index, self.data):
                result.row()
        result.row()
        result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()
