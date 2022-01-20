from apps.feedback.bots.commands.echo import HelloCommand
from apps.feedback.bots.commands.get_main_menu import GetMainMenuCommand
from vkbottle.bot import Message

from apps.feedback.bots.vk.base import BaseVkBot


def init_endpoints(app: BaseVkBot):
    @app.bot.on.message(text="Привет")
    async def echo(message: Message):
        result = await HelloCommand(user_id=message.peer_id).execute()
        await app.send_response(result, message)

    @app.bot.on.message(text=["Начать", "Главное меню"])
    async def get_main_menu(message: Message):
        result = await GetMainMenuCommand().execute()
        await app.send_response(result, message)
