from abc import ABC, abstractmethod
from typing import Union
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage


class BaseTelegramBot(ABC):
    bot: Bot
    dp: Dispatcher

    @abstractmethod
    def send_response(self, response: Union[SingleMessage, MultipleMessages], message: Message) -> None:
        pass
