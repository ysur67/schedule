from abc import ABC, abstractmethod
from typing import Any, Dict, Union, List
from collections.abc import Iterable


class BaseKeyboard(ABC):

    def __init__(self, initial: Any, is_inline: bool = False, has_cancel_button: bool = True) -> None:
        self.data = initial
        self.is_inline = is_inline
        self.has_cancel_button = has_cancel_button

    @abstractmethod
    def to_vk_api(self) -> Union[str, List[str]]:
        return self.result.get_json()

    def _is_last(self, index: int, data: Iterable) -> bool:
        if not isinstance(data, Iterable):
            return False
        return index == len(data) - 1
