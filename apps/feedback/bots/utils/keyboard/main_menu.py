from typing import List, Union, Any

from vkbottle import Keyboard, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .base import BaseKeyboard


class MainMenuKeyboard(BaseKeyboard):
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
