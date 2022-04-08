from functools import singledispatchmethod
from typing import Any, Dict, Iterable, List, Union

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.base import SingleMessage
from apps.feedback.bots.telegram.app import init_endpoints
from apps.feedback.bots.telegram.filters import (EducationalLevelExistFilter,
                                                 GroupExistFilter)
from apps.feedback.bots.telegram.middlewares import CreateAccountMiddleware

from .base import TelegramBotMixin


class TelegramBot(BaseBot, TelegramBotMixin):
    FILTERS = [GroupExistFilter, EducationalLevelExistFilter]

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.dp.middleware.setup(CreateAccountMiddleware())
        for item in self.FILTERS:
            self.dp.bind_filter(
                item,
                event_handlers=[
                    self.dp.message_handlers,
                    self.dp.callback_query_handlers
                ]
            )
        init_endpoints(self)

    def listen(self) -> None:
        executor.start_polling(self.dp, skip_updates=True)

    async def send_response(self, response: List[Dict], message: Message) -> None:
        return [await message.answer(**item) for item in response]

    async def send_message(self, message: SingleMessage, user_id: int) -> None:
        return await self.bot.send_message(chat_id=user_id, **message.to_dict())

    async def send_messages(self, message: Iterable[SingleMessage], user_id: int) -> None:
        return [await self.bot.send_message(user_id=user_id, message=item) for item in message]
