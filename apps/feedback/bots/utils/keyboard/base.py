from abc import ABC, abstractmethod
from typing import Any
from vkbottle import Keyboard
from collections.abc import Iterable


class BaseKeyboard(ABC):
    result: Keyboard

    @classmethod
    def build_instance(cls, data: Any) -> None:
        instance = cls(data)
        instance.init_keyboard()
        return instance

    def __init__(self, initial: Any) -> None:
        self.data = initial

    @abstractmethod
    def init_keyboard(self) -> Keyboard:
        pass

    def to_api(self) -> str:
        return self.result.get_json()

    def _is_last(self, index: int) -> bool:
        if not isinstance(self.data, Iterable):
            return False
        return index == len(self.data) - 1
