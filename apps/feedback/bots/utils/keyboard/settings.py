from typing import Iterable, List, Union

from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)
from vkbottle import Keyboard, Text
from vkbottle.tools.dev.keyboard.color import KeyboardButtonColor

from .base import Button


class SettingsKeyboard:
    data: Iterable[Button]

    def to_vk_api(self) -> Union[str, List[str]]:
        result = Keyboard(inline=self.is_inline)
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index, self.data):
                result.row()
        result.row()
        result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()

    def to_telegram_api(self) -> Union[ReplyKeyboardMarkup, List[InlineKeyboardMarkup]]:
        result = ReplyKeyboardMarkup(resize_keyboard=True)
        for index, value in enumerate(self.data):
            result.add(KeyboardButton(value.title))
            if not self._is_last(index, self.data):
                result.row()
        result.row()
        result.add(KeyboardButton("Главное меню"))
        return result
