from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Optional, Union
from apps.feedback.bots.utils.const import Messengers
from dataclasses import dataclass


@dataclass
class SingleMessage:
    message: str
    keyboard: Optional[Any] = None

    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "keyboard": self.keyboard
        }


@dataclass
class MultipleMessages:
    messages: Iterable[SingleMessage]


class BaseCommand(ABC):
    type: Messengers

    def __init__(self, messenger: Messengers = Messengers.VK, **kwargs) -> None:
        self.type = messenger
        self.kwargs = kwargs

    async def execute(self) -> Union[SingleMessage, MultipleMessages]:
        if self.type == Messengers.VK:
            return await self._vk_execute()
        raise NotImplementedError(f"There is no approach for type {self.type}")

    @abstractmethod
    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        pass

    def _require_field(self, key: str, raise_exception: bool = True) -> Any:
        result = self.kwargs.get(key, None)
        if result is not None:
            return result
        if raise_exception:
            raise ValueError(f"You should provide {key} kwarg for this command")
        return result

