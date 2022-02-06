from datetime import datetime
from apps.feedback.bots.commands.educational_levels import \
    EducationalLevelsCommand
from apps.feedback.bots.commands.get_groups_by_level_command import \
    GetGroupsByLevelCommand
from apps.feedback.bots.commands.get_schedule import GetScheduleCommand
from apps.feedback.bots.telegram.base import BaseTelegramBot
from apps.feedback.bots.telegram.filters.educational_level_exist import EducationalLevelExistFilter
from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.mappers.telegram import ToTelegramApiMapper
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from apps.feedback.bots.telegram.states import UserStates


def init_endpoints(app: BaseTelegramBot):

    @app.dp.message_handler(
        Text(equals=["Уровень", "Выбор группы", "Выбрать группу"], ignore_case=True),
        state="*"
    )
    async def get_educational_levels(message: Message):
        result = await EducationalLevelsCommand().execute()
        user = message.from_user
        state = app.dp.current_state(user=user.id)
        await state.set_state(UserStates.CHOOSE_GROUP_STATE)
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        EducationalLevelExistFilter(),
        state=UserStates.CHOOSE_GROUP_STATE
    )
    async def get_groups(message: Message):
        result = await GetGroupsByLevelCommand(message=message.text).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        Text(equals=["Показать расписание"], ignore_case=True),
        state="*"
    )
    async def show_schedule(message: Message):
        result = await GetScheduleCommand(
            messenger=Messengers.TELEGRAM,
            date_start=datetime.now().date(),
            account_id=message.from_user.id
        ).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)
