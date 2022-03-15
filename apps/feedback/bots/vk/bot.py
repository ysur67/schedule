from functools import singledispatchmethod
from typing import Any, Dict, Iterable, List, Union

from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.base import SingleMessage
from apps.feedback.bots.vk.app import init_endpoints
from apps.feedback.bots.vk.base import BaseVkBot
from apps.feedback.bots.vk.middlewares.create_account import \
    CreateAccountMiddleware
from vkbottle.bot import Bot, Message


class VkBot(BaseBot, BaseVkBot):

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(self.token)
        self.bot.labeler.message_view.register_middleware(
            CreateAccountMiddleware)
        init_endpoints(self)

    def listen(self) -> None:
        self.bot.run_forever()

    @singledispatchmethod
    async def send_message(self, messages: Iterable[SingleMessage], user_id: int) -> None:
        raise NotImplementedError(
            f"There is no approach for type {type(messages)}")

    @send_message.register(SingleMessage)
    async def _(self, messages: SingleMessage, user_id: int) -> None:
        return await self.bot.api.messages.send(peer_id=user_id, random_id=0, **messages.to_dict())

    @send_message.register(list)
    async def _(self, messages: 'list[SingleMessage]', user_id: int) -> None:
        return await [self.send_message(item, user_id) for item in messages]

    @singledispatchmethod
    async def send_response(self, response: Union[Dict, List[Dict]], message: Message) -> None:
        raise NotImplementedError(
            f"There is no approach for type {type(response)}")

    @send_response.register(dict)
    async def _(self, response: Dict, message: Message) -> None:
        return await message.answer(**response)

    @send_response.register(list)
    async def _(self, response: List[Dict], message: Message) -> None:
        return [await message.answer(**item) for item in response]
