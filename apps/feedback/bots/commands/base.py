from abc import ABC, abstractmethod
from typing import Any, Dict
from apps.feedback.bots.utils.const import Messengers

class BaseCommand(ABC):
    type: Messengers

    def __init__(self, messenger: Messengers = Messengers.VK, **kwargs) -> None:
        self.type = messenger
        self.kwargs = kwargs

    async def execute(self) -> Dict:
        if self.type == Messengers.VK:
            return await self._vk_execute()
        raise NotImplementedError(f"There is no approach for type {self.type}")

    @abstractmethod
    async def _vk_execute(self) -> Dict:
        pass

    def _require_field(self, key: str, raise_exception: bool = True) -> Any:
        result = self.kwargs.get(key, None)
        if result is not None:
            return result
        if raise_exception:
            raise ValueError(f"You should provide {key} kwarg for this command")
        return result
