from apps.feedback.bots.commands.change_days_offset import SetDaysOffsetCommand
from apps.feedback.bots.commands.get_change_days_offset_info import GetChangeDaysOffsetInfoCommand
from apps.feedback.bots.commands.get_current_status import GetCurrentStatusCommand
from apps.feedback.bots.commands.get_settings import GetSettingsCommand
from apps.feedback.bots.commands.save_current_group_to_user import SaveCurrentGroupCommand
from apps.feedback.bots.commands.turn_off_notifications import TurnOffNotificationsCommand
from apps.feedback.bots.commands.turn_on_notifications import TurnOnNotificationsCommand
from apps.feedback.bots.vk.base import BaseVkBot
from apps.feedback.bots.vk.rules.group_rule import GroupExistRule
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.bot import Message


def init_endpoints(app: BaseVkBot):
    @app.bot.on.message(GroupExistRule())
    async def save_current_group(message: Message):
        result = await SaveCurrentGroupCommand(
            group=message.text,
            account_id=message.peer_id
        ).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Статус")
    async def get_current_profile_status(message: Message):
        result = await GetCurrentStatusCommand(account_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Настройки")
    async def get_settings(message: Message):
        result = await GetSettingsCommand(account_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Включить уведомления о занятиях")
    async def turn_on_notifications(message: Message):
        result = await TurnOnNotificationsCommand(account_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Отключить уведомления о занятиях")
    async def turn_off_notifications(message: Message):
        result = await TurnOffNotificationsCommand(account_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text="Изменить кол-во дней на расписание")
    async def get_change_offset_info(message: Message):
        result = await GetChangeDaysOffsetInfoCommand(account_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(CommandRule("Получать на", ["!"], 1))
    async def change_days_offset(message: Message, args: 'tuple[str]'):
        result = await SetDaysOffsetCommand(
            account_id=message.peer_id, days_offset=args[0]
        ).execute()
        await app.send_response(result, message)