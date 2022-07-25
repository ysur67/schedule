from typing import List, Union

from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)
from apps.timetables.models import EducationalLevel
from django.db.models.query import QuerySet
from vkbottle import Keyboard, KeyboardButtonColor, Text


class EducationalLevelsKeyboard:
    data: QuerySet[EducationalLevel]

    def to_vk_api(self) -> str:
        result = Keyboard()
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            if not self._is_last(index, self.data):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()

    def to_telegram_api(self) -> Union[ReplyKeyboardMarkup, List[InlineKeyboardMarkup]]:
        result = ReplyKeyboardMarkup()
        for index, value in enumerate(self.data):
            result.add(KeyboardButton(value.title))
            if not self._is_last(index, self.data):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(KeyboardButton("Главное меню"))
        return result
