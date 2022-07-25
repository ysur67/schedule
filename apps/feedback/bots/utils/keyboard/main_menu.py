from typing import Any, List, Union

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from vkbottle import Keyboard, Text


class MainMenuKeyboard:
    data: List[str]

    def to_vk_api(self) -> Union[str, List[str]]:
        result = Keyboard(inline=self.is_inline)
        for index, value in enumerate(self.data):
            result.add(Text(value))
            if not self._is_last(index, self.data):
                result.row()
        return result.get_json()

    def to_telegram_api(self) -> ReplyKeyboardMarkup:
        result = ReplyKeyboardMarkup(resize_keyboard=True)
        for index, value in enumerate(self.data):
            result.add(KeyboardButton(value))
            if not self._is_last(index, self.data):
                result.row()
        return result
