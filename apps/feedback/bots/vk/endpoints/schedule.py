from datetime import datetime

from apps.feedback.bots.commands.educational_levels import \
    EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import \
    GetGroupsByLevelCommand
from apps.feedback.bots.commands.get_schedule import GetScheduleCommand
from apps.feedback.bots.utils.mappers.vk import ToVkApiMapper
from apps.feedback.bots.vk.base import VkBotMixin
from apps.feedback.bots.vk.rules.educational_level_rule import \
    EducationalLevelExistRule
from apps.feedback.bots.vk.states import UserStates
from asgiref.sync import sync_to_async
from vkbottle.bot import Message


def init_endpoints(app: VkBotMixin):

    @app.bot.on.message(text=["Уровень", "Выбор группы", "Выбрать группу"])
    async def get_educational_levels(message: Message):
        result = await EducationalLevelsCommand().execute()
        await app.bot.state_dispenser.set(message.peer_id, UserStates.CHOOSE_GROUP_STATE)
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(EducationalLevelExistRule())
    async def get_groups(message: Message):
        result = await GetGroupsByLevelCommand(message=message.text).execute()
        messages = await app.send_response(await ToVkApiMapper.convert(result), message)
        await app.bot.state_dispenser.set(
            message.peer_id,
            UserStates.CHOOSE_GROUP_STATE,
            messages=messages
        )

    @app.bot.on.message(text="Показать расписание")
    async def show_schedule(message: Message):
        result = await GetScheduleCommand(
            date_start=datetime.now(),
            account_id=message.peer_id
        ).execute()
        await app.send_response(await ToVkApiMapper.convert(result), message)
