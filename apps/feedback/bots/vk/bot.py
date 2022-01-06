from vkbottle.bot import Bot, Message
from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.echo import HelloCommand
from apps.feedback.bots.commands.educational_levels import EducationalLevelsCommand
from apps.feedback.bots.vk.keyboard import EducationalLevelsKeyboard, GroupsKeyboard
from apps.feedback.bots.vk.rules.educational_level_rule import EducationalLevelExistRule
from apps.timetables.usecases.educational_level import get_all_educational_levels, get_educational_level_by_title
from asgiref.sync import sync_to_async


class VkBot(BaseBot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(self.token)
        self.init_commands()

    def listen(self) -> None:
        self.bot.run_forever()

    def init_commands(self) -> None:
        @self.bot.on.message(text="Привет")
        async def echo(message: Message):
            await message.answer(HelloCommand(message.peer_id).execute())

        @self.bot.on.message(text="Уровень")
        async def get_educational_levels(message: Message):
            _keyboard = sync_to_async(EducationalLevelsKeyboard)
            keyboard = await _keyboard(levels=get_all_educational_levels())
            await message.answer(EducationalLevelsCommand().execute(), keyboard=keyboard.to_api())

        @self.bot.on.message(EducationalLevelExistRule())
        async def get_groups(message: Message):
            _keyboard = sync_to_async(GroupsKeyboard)
            _get_level = sync_to_async(get_educational_level_by_title)
            level = await _get_level(message.text)
            keyboard = await _keyboard(level=level)
            await message.answer("asdfasdfasfdsakjl", keyboard=keyboard.to_api())
