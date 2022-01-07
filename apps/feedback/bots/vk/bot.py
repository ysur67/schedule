from vkbottle.bot import Bot, Message
from apps.feedback.bots import BaseBot
from apps.feedback.bots.commands.echo import HelloCommand
from apps.feedback.bots.commands.educational_levels import EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import GetGroupsByLevelCommand
from apps.feedback.bots.vk.rules.educational_level_rule import EducationalLevelExistRule


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
            result = await HelloCommand(user_id=message.peer_id).execute()
            await message.answer(**result)

        @self.bot.on.message(text=["Уровень", "Главное меню"])
        async def get_educational_levels(message: Message):
            result = await EducationalLevelsCommand().execute()
            await message.answer(**result)

        @self.bot.on.message(EducationalLevelExistRule())
        async def get_groups(message: Message):
            result = await GetGroupsByLevelCommand(message=message.text).execute()
            await message.answer(**result)
