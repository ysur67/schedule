from abc import ABC, abstractmethod
from typing import Union
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage


class BaseBot(ABC):

    def __init__(self, token: str) -> None:
        self.token = token

    @abstractmethod
    def listen(self) -> None:
        return

    @abstractmethod
    async def send_message(self, message: Union[SingleMessage, MultipleMessages], user_id: int) -> None:
        return
