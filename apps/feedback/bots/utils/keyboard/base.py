from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from vkbottle import Keyboard, KeyboardButtonColor, Text


class BaseKeyboard(ABC):

    def __init__(self, initial: Any, is_inline: bool = False, has_cancel_button: bool = True) -> None:
        self.data = initial
        self.is_inline = is_inline
        self.has_cancel_button = has_cancel_button

    @abstractmethod
    def to_vk_api(self) -> Union[str, List[str]]:
        pass

    @abstractmethod
    def to_telegram_api(self) -> Union[ReplyKeyboardMarkup, List[InlineKeyboardMarkup]]:
        pass

    def _is_last(self, index: int, data: Iterable) -> bool:
        if not isinstance(data, Iterable):
            return False
        return index == len(data) - 1


@dataclass
class Button:
    title: str
    value: Optional[str]


@dataclass
class IKeyboard(ABC):
    data: Iterable[Button] = []
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
