from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message
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
from apps.feedback.bots.telegram.base import TelegramBotMixin
from apps.feedback.bots.telegram.filters.group_exist import GroupExistFilter
from apps.feedback.bots.telegram.states import UserStates
from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.mappers.telegram import ToTelegramApiMapper


def init_endpoints(app: TelegramBotMixin):
    @app.dp.callback_query_handler(
        GroupExistFilter(),
        state=UserStates.CHOOSE_GROUP_STATE
    )
    async def save_current_group_from_callback(obj: CallbackQuery):
        user = obj.from_user
        result = await SaveCurrentGroupCommand(
            messenger=Messengers.TELEGRAM,
            group=obj.data,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await obj.answer(text="Выбор успешно сохранен")
        await app.send_messages(await ToTelegramApiMapper.convert(result), user.id)

    @app.dp.message_handler(
        GroupExistFilter(),
        state=UserStates.CHOOSE_GROUP_STATE
    )
    async def save_current_group_from_message(message: Message):
        user = message.from_user
        result = await SaveCurrentGroupCommand(
            messenger=Messengers.TELEGRAM,
            group=message.text,
            account_id=user.id
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(Text(equals=["статус"], ignore_case=True), state="*")
    async def get_current_profile_status(message: Message):
        result = await GetCurrentStatusCommand(
            messenger=Messengers.TELEGRAM,
            account_id=message.from_user.id
        ).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(Text(equals=["настройки"], ignore_case=True), state="*")
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
        Text(startswith=["!Получать на"], ignore_case=True),
        state=UserStates.CHANGE_DAYS_OFFSET_STATE
    )
    async def change_days_offset(message: Message):
        user = message.from_user
        days_offset = message.text.split(" ")[-1]
        result = await SetDaysOffsetCommand(
            messenger=Messengers.TELEGRAM,
            account_id=user.id,
            days_offset=days_offset
        ).execute()
        state = app.dp.current_state(user=user.id)
        await state.reset_state()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)
