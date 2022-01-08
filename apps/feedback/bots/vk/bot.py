from typing import Any
from vkbottle.bot import Bot, Message
from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage
from apps.feedback.bots.commands.echo import HelloCommand
from apps.feedback.bots.commands.educational_levels import EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import GetGroupsByLevelCommand
from apps.feedback.bots.commands.save_current_group_to_user import SaveCurrentGroupCommand
from apps.feedback.bots.vk.middlewares.get_or_create_profile import CreateAccountMiddleware
from apps.feedback.bots.vk.rules.educational_level_rule import EducationalLevelExistRule
from functools import singledispatchmethod

from apps.feedback.bots.vk.rules.group_rule import GroupExistRule


class VkBot(BaseBot):

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(self.token)
        self.bot.labeler.message_view.register_middleware(CreateAccountMiddleware)
        self.init_commands()

    def listen(self) -> None:
        self.bot.run_forever()

    def init_commands(self) -> None:
        @self.bot.on.message(text="Привет")
        async def echo(message: Message):
            result = await HelloCommand(user_id=message.peer_id).execute()
            await self._send_response(result, message)

        @self.bot.on.message(text=["Уровень", "Главное меню", "Начать"])
        async def get_educational_levels(message: Message):
            result = await EducationalLevelsCommand().execute()
            await self._send_response(result, message)

        @self.bot.on.message(EducationalLevelExistRule())
        async def get_groups(message: Message):
            result = await GetGroupsByLevelCommand(message=message.text).execute()
            await self._send_response(result, message)

        @self.bot.on.message(GroupExistRule())
        async def save_current_group(message: Message):
            result = await SaveCurrentGroupCommand(group=message.text).execute()
            await self._send_response(result, message)

    @singledispatchmethod
    async def _send_response(self, response: Any, message: Message) -> None:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

    @_send_response.register(SingleMessage)
    async def _(self, response: SingleMessage, message: Message) -> None:
        return await message.answer(**response.to_dict())

    @_send_response.register(MultipleMessages)
    async def _(self, response: MultipleMessages, message: Message) -> None:
        for item in response.messages:
            await message.answer(**item.to_dict())
