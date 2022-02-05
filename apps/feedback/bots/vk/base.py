from abc import ABC, abstractmethod
from typing import Any

from vkbottle.bot import Bot, Message


class BaseVkBot(ABC):
    bot: Bot

    @abstractmethod
    def send_response(self, response: Any, message: Message) -> None:
        pass
