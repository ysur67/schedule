from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from vkbottle.bot import Bot, Message


class VkBotMixin(ABC):
    bot: Bot

    @abstractmethod
    async def send_response(self, response: Iterable[Dict], message: Message) -> None:
        pass
