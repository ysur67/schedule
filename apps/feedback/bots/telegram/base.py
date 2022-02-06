from abc import ABC, abstractmethod
from typing import Dict, List, Union

from aiogram import Bot, Dispatcher
from aiogram.types import Message


class BaseTelegramBot(ABC):
    bot: Bot
    dp: Dispatcher

    @abstractmethod
    def send_response(self, response: Union[Dict, List[Dict]], message: Message) -> None:
        pass
