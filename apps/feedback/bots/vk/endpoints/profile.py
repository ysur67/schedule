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
from apps.feedback.bots.utils.mappers.vk import ToVkApiMapper
from apps.feedback.bots.vk.base import VkBotMixin
from apps.feedback.bots.vk.rules.group_rule import GroupExistRule
from apps.feedback.bots.vk.states import UserStates
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import CommandRule


def init_endpoints(app: VkBotMixin):
    @app.bot.on.message(GroupExistRule(), state=UserStates.CHOOSE_GROUP_STATE)
    async def save_current_group(message: Message):
        result = await SaveCurrentGroupCommand(
            group=message.text,
            account_id=message.peer_id
        ).execute()
        await app.bot.state_dispenser.delete(message.peer_id)
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(text="Статус")
    async def get_current_profile_status(message: Message):
        result = await GetCurrentStatusCommand(account_id=message.peer_id).execute()
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(text="Настройки")
    async def get_settings(message: Message):
        result = await GetSettingsCommand(account_id=message.peer_id).execute()
        await app.bot.state_dispenser.set(message.peer_id, UserStates.CHANGE_SETTINGS_STATE)
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(
        text="Включить уведомления о занятиях",
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def turn_on_notifications(message: Message):
        result = await TurnOnNotificationsCommand(account_id=message.peer_id).execute()
        await app.bot.state_dispenser.delete(message.peer_id)
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(
        text="Отключить уведомления о занятиях",
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def turn_off_notifications(message: Message):
        result = await TurnOffNotificationsCommand(account_id=message.peer_id).execute()
        await app.bot.state_dispenser.delete(message.peer_id)
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(
        text="Изменить кол-во дней на расписание",
        state=UserStates.CHANGE_SETTINGS_STATE
    )
    async def get_change_offset_info(message: Message):
        result = await GetChangeDaysOffsetInfoCommand(account_id=message.peer_id).execute()
        await app.bot.state_dispenser.set(
            message.peer_id,
            state=UserStates.CHANGE_DAYS_OFFSET_STATE
        )
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(
        CommandRule("Получать на", ["!"], 1),
        state=UserStates.CHANGE_DAYS_OFFSET_STATE
    )
    async def change_days_offset(message: Message, args: 'tuple[str]'):
        result = await SetDaysOffsetCommand(
            account_id=message.peer_id, days_offset=args[0]
        ).execute()
        await app.bot.state_dispenser.delete(message.peer_id)
        await app.send_response(await ToVkApiMapper.convert(result), message)
