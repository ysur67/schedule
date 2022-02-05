from functools import singledispatchmethod
from apps.feedback.bots import BaseBot
from typing import Union, Any, Dict, List
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage
from apps.feedback.bots.telegram.app import init_endpoints
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from .base import BaseTelegramBot


class TelegramBot(BaseBot, BaseTelegramBot):

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        init_endpoints(self)

    def listen(self) -> None:
        executor.start_polling(self.dp, skip_updates=True)

    @singledispatchmethod
    async def send_response(self, response: Any, message: Message) -> None:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

    @send_response.register(dict)
    async def _(self, response: Dict, message: Message) -> None:
        return await message.answer(**response)

    @send_response.register(list)
    async def _(self, response: List[Dict], message: Message) -> None:
        return [await message.answer(**item) for item in response]

    @singledispatchmethod
    async def send_message(self, message: Union[SingleMessage, MultipleMessages], user_id: int) -> None:
        raise NotImplementedError(f"There is no approach for type {type(message)}")

    @send_message.register(SingleMessage)
    async def _(self, message: SingleMessage, user_id: int) -> None:
        return await self.bot.send_message(chat_id=user_id, **message.to_dict())

    @send_message.register(MultipleMessages)
    async def _(self, message: MultipleMessages, user_id: int) -> None:
        return [await self.bot.send_message(chat_id=user_id, *item.to_dict().values()) for item in message.messages]
