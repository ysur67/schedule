from datetime import datetime
from apps.feedback.bots.commands.educational_levels import \
    EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import \
    GetGroupsByLevelCommand
from apps.feedback.bots.commands.get_schedule import GetScheduleCommand
from apps.feedback.bots.telegram.base import BaseTelegramBot
from apps.feedback.bots.utils.mappers.telegram import ToTelegramApiMapper
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from apps.feedback.bots.telegram.states import UserStates


def init_endpoints(app: BaseTelegramBot):

    @app.dp.message_handler(
        Text(equals=["Уровень", "Выбор группы", "Выбрать группу"], ignore_case=True)
    )
    async def get_educational_levels(message: Message):
        result = await EducationalLevelsCommand().execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(state=UserStates.CHOOSE_GROUP_STATE)
    async def get_groups(message: Message):
        result = await GetGroupsByLevelCommand(message=message.text).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(Text(equals=["Показать расписание"], ignore_case=True))
    async def show_schedule(message: Message):
        result = await GetScheduleCommand(
            date_start=datetime.now().date(),
            account_id=message.from_user.id
        ).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)
