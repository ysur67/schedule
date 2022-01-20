from typing import Any
from vkbottle.bot import Bot, Message
from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage
from apps.feedback.bots.vk.app import init_endpoints
from apps.feedback.bots.vk.base import BaseVkBot
from apps.feedback.bots.vk.middlewares.create_account import CreateAccountMiddleware
from functools import singledispatchmethod


class VkBot(BaseBot, BaseVkBot):

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(self.token)
        self.bot.labeler.message_view.register_middleware(CreateAccountMiddleware)
        init_endpoints(self)

    def listen(self) -> None:
        self.bot.run_forever()

    @singledispatchmethod
    async def send_response(self, response: Any, message: Message) -> None:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

    @send_response.register(SingleMessage)
    async def _(self, response: SingleMessage, message: Message) -> None:
        return await message.answer(**response.to_dict())

    @send_response.register(MultipleMessages)
    async def _(self, response: MultipleMessages, message: Message) -> None:
        for item in response.messages:
            await message.answer(**item.to_dict())
