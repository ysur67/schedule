from apps.feedback.bots.commands.get_main_menu import GetMainMenuCommand
from apps.feedback.bots.telegram.base import BaseTelegramBot
from aiogram.types import Message
from apps.feedback.bots.commands.show_id import ShowIDCommand
from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.mappers.telegram import ToTelegramApiMapper


def init_endpoints(app: BaseTelegramBot):

    @app.dp.message_handler(commands=["show_id"])
    async def echo(message: Message):
        result = await ShowIDCommand(user_id=message.from_user.id).execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)

    @app.dp.message_handler(commands=["start"])
    async def get_main_menu(message: Message):
        result = await GetMainMenuCommand().execute()
        await app.send_response(await ToTelegramApiMapper.convert(result), message)
