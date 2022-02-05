from typing import List, Union

from vkbottle import Keyboard, Text

from .base import BaseKeyboard


class MainMenuKeyboard(BaseKeyboard):

    def to_vk_api(self) -> Union[str, List[str]]:
        result = Keyboard(inline=self.is_inline)
        self.data: List[str]
        for index, value in enumerate(self.data):
            result.add(Text(value))
            if not self._is_last(index, self.data):
                result.row()
        return result.get_json()
