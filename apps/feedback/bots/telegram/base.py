from abc import ABC, abstractmethod
from typing import Dict, List

from aiogram import Bot, Dispatcher
from aiogram.types import Message


class TelegramBotMixin(ABC):
    bot: Bot
    dp: Dispatcher

    @abstractmethod
    async def send_response(self, response: List[Dict], message: Message) -> List[Message]:
        pass
