from abc import ABC, abstractmethod
from typing import Any, Dict
from vkbottle import Keyboard
from collections.abc import Iterable


class BaseKeyboard(ABC):

    def __init__(self, initial: Any, **kwargs: Dict) -> None:
        self.data = initial

    @abstractmethod
    def to_vk_api(self) -> str:
        return self.result.get_json()

    def _is_last(self, index: int) -> bool:
        if not isinstance(self.data, Iterable):
            return False
        return index == len(self.data) - 1
