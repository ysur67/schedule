from abc import ABC, abstractmethod
from typing import Any
from vkbottle.bot import Message, Bot


class BaseVkBot(ABC):
    bot: Bot

    @abstractmethod
    def send_response(self, response: Any, message: Message) -> None:
        pass
