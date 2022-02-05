from apps.feedback.bots.telegram.base import BaseTelegramBot
from aiogram.types import Message
from apps.feedback.bots.commands.show_id import ShowIDCommand
from apps.feedback.bots.utils.const import Messengers


def init_endpoints(app: BaseTelegramBot):

    @app.dp.message_handler(commands=["Привет", "Покажи мой ID"])
    async def echo(message: Message):
        result = await ShowIDCommand(
            Messengers.TELEGRAM, user_id=message.from_user.id
        ).execute()
        await app.send_response(result, message)
