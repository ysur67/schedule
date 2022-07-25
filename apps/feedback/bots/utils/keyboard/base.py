from abc import ABC
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import List, Optional, Union

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from vkbottle import Keyboard, KeyboardButtonColor, Text


@dataclass
class Button:
    title: str
    value: Optional[str] = None


# Чтобы имя класса не конфликтовало с Keybord'ами из пакетов
@dataclass
class SimpleKeyboard(ABC):
    data: Iterable[Button] = field(
        default_factory=list,
    )
    is_inline: bool = False
    has_cancel_button: bool = True
    items_per_row: int = 2

    def __post_init__(self) -> None:
        assert len(self.data) > 0, "Keyboard data can't be empty!"

    def to_telegram_api(self) -> Union[ReplyKeyboardMarkup, List[InlineKeyboardMarkup]]:
        result = InlineKeyboardMarkup() if self.is_inline else ReplyKeyboardMarkup(
            resize_keyboard=True)
        result.row_width = self.items_per_row
        for index, value in enumerate(self.data):
            title = value.title
            cancel_button = InlineKeyboardButton(
                title, callback_data=title) if self.is_inline else KeyboardButton(title)
            result.insert(cancel_button)
            should_insert_row = (index + 1) % self.items_per_row == 0
            if should_insert_row and not is_last_in_iterable(index, self.data):
                result.row()
        if self.has_cancel_button:
            cancel_button = InlineKeyboardButton(
                'Главное меню', callback_data='Главное меню'
            ) if self.is_inline else KeyboardButton('Главное меню')
            result.add(cancel_button)
        return result

    def to_vk_api(self) -> str:
        result = Keyboard(inline=self.is_inline)
        for index, value in enumerate(self.data):
            result.add(Text(value.title))
            should_insert_row = (index + 1) % self.items_per_row == 0
            if should_insert_row and not is_last_in_iterable(index, self.data):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()


def is_last_in_iterable(index: int, data: Iterable) -> bool:
    if not isinstance(data, Iterable):
        return False
    return index == len(data) - 1
