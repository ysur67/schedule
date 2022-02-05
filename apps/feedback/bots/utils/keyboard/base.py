from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Dict, List, Union


class BaseKeyboard(ABC):

    def __init__(self, initial: Any, is_inline: bool = False, has_cancel_button: bool = True) -> None:
        self.data = initial
        self.is_inline = is_inline
        self.has_cancel_button = has_cancel_button

    @abstractmethod
    def to_vk_api(self) -> Union[str, List[str]]:
        pass

    def _is_last(self, index: int, data: Iterable) -> bool:
        if not isinstance(data, Iterable):
            return False
        return index == len(data) - 1


@dataclass
class Button:
    title: str
