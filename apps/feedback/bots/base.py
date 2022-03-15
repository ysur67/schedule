from abc import ABC, abstractmethod
from typing import Iterable, Union

from apps.feedback.bots.commands.base import SingleMessage


class BaseBot(ABC):

    def __init__(self, token: str) -> None:
        self.token = token

    @abstractmethod
    def listen(self) -> None:
        return

    @abstractmethod
    async def send_message(self, message: Iterable[SingleMessage], user_id: int) -> None:
        return
