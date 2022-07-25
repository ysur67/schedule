from abc import ABC, abstractmethod
from ast import List
from typing import Any, Dict

from apps.feedback.bots.utils.response.message import SingleMessage


class Response(ABC):

    def __init__(self, data: List[SingleMessage]) -> None:
        self.data = data

    @abstractmethod
    def to_vk_api(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def to_telegram_api(self) -> List[Dict[str, Any]]:
        pass
