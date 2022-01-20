import datetime
from apps.feedback.bots.commands.educational_levels import EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import GetGroupsByLevelCommand
from apps.feedback.bots.commands.get_schedule import GetScheduleCommand
from vkbottle.bot import Message
from apps.feedback.bots.vk.base import BaseVkBot
from apps.feedback.bots.vk.rules.educational_level_rule import EducationalLevelExistRule


def init_endpoints(app: BaseVkBot):

    @app.bot.on.message(text=["Уровень", "Выбор группы", "Выбрать группу"])
    async def get_educational_levels(message: Message):
        result = await EducationalLevelsCommand().execute()
        await app.send_response(result, message)

    @app.bot.on.message(EducationalLevelExistRule())
    async def get_groups(message: Message):
        result = await GetGroupsByLevelCommand(message=message.text).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Показать расписание")
    async def show_schedule(message: Message):
        result = await GetScheduleCommand(
            date_start=datetime.now().date(),
            account_id=message.peer_id
        ).execute()
        await app.send_response(result, message)
