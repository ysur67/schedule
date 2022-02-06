from apps.feedback.bots.commands.change_days_offset import SetDaysOffsetCommand
from apps.feedback.bots.commands.get_change_days_offset_info import \
    GetChangeDaysOffsetInfoCommand
from apps.feedback.bots.commands.get_current_status import \
    GetCurrentStatusCommand
from apps.feedback.bots.commands.get_settings import GetSettingsCommand
from apps.feedback.bots.commands.save_current_group_to_user import \
    SaveCurrentGroupCommand
from apps.feedback.bots.commands.turn_off_notifications import \
    TurnOffNotificationsCommand
from apps.feedback.bots.commands.turn_on_notifications import \
    TurnOnNotificationsCommand

from aiogram.types import Message
from apps.feedback.bots.telegram.base import BaseTelegramBot
from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.mappers.telegram import ToTelegramApiMapper
from apps.feedback.bots.telegram.states import UserStates
from aiogram.dispatcher.filters import Text


def init_endpoints(app: BaseTelegramBot):
    @app.dp.message_handler(state=UserStates.CHOOSE_GROUP_STATE)
    async def save_current_group(message: Message):
        user = message.from_user
        result = await SaveCurrentGroupCommand(
            messenger=Messengers.TELEGRAM,
            group=message.text,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(Text(equals=["статус"], ignore_case=True))
    async def get_current_profile_status(message: Message):
        result = await GetCurrentStatusCommand(
            messenger=Messengers.TELEGRAM,
            account_id=message.from_user.id
        ).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(Text(equals=["настройки"], ignore_case=True))
    async def get_settings(message: Message):
        result = await GetSettingsCommand(
            messenger=Messengers.TELEGRAM,
            account_id=message.from_user.id
        ).execute()
        state = app.dp.current_state(user=message.from_user.id)
        await state.set_state(UserStates.CHANGE_SETTINGS_STATE)
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        Text(equals=["Включить уведомления о занятиях"], ignore_case=True),
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def turn_on_notifications(message: Message):
        user = message.from_user
        result = await TurnOnNotificationsCommand(
            messenger=Messengers.TELEGRAM,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        Text(equals=["Отключить уведомления о занятиях"], ignore_case=True),
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def turn_off_notifications(message: Message):
        user = message.from_user
        result = await TurnOffNotificationsCommand(
            messenger=Messengers.TELEGRAM,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        Text(equals=["Изменить кол-во дней на расписание"], ignore_case=True),
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def get_change_offset_info(message: Message):
        user = message.from_user
        result = await GetChangeDaysOffsetInfoCommand(
            messenger=Messengers.TELEGRAM,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.set_state(UserStates.CHANGE_DAYS_OFFSET_STATE)
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(
        commands=["/Получать на"],
        state=UserStates.CHANGE_DAYS_OFFSET_STATE
    )
    async def change_days_offset(message: Message):
        print(message.get_args())
        # result = await SetDaysOffsetCommand(
        #     account_id=message.peer_id, days_offset=args[0]
        # ).execute()
        # await app.bot.state_dispenser.delete(message.peer_id)
        # await app.send_response(await ToTelegramApiMapper.convert(result), message)
