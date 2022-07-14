from abc import ABC, abstractmethod
from typing import Iterable

from apps.feedback.bots.utils.response.message import SingleMessage


class BaseBot(ABC):

    def __init__(self, token: str) -> None:
        self.token = token

    @abstractmethod
    def listen(self) -> None:
        return

    @abstractmethod
    async def send_messages(self, messages: Iterable[SingleMessage], user_id: int) -> None:
        return

    @abstractmethod
    async def send_message(self, message: SingleMessage, user_id: int) -> None:
        return
