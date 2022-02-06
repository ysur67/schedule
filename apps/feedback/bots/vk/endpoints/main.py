from vkbottle.bot import Message

from apps.feedback.bots.commands.get_main_menu import GetMainMenuCommand
from apps.feedback.bots.commands.show_id import ShowIDCommand
from apps.feedback.bots.utils.mappers.vk import ToVkApiMapper
from apps.feedback.bots.vk.base import BaseVkBot


def init_endpoints(app: BaseVkBot):
    @app.bot.on.message(text=["Привет", "Покажи мой ID"])
    async def echo(message: Message):
        result = await ShowIDCommand(user_id=message.peer_id).execute()
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(text=["Начать", "Главное меню"])
    async def get_main_menu(message: Message):
        result = await GetMainMenuCommand().execute()
        # TODO: custom state dispenser
        try:
            await app.bot.state_dispenser.delete(message.peer_id)
        except KeyError:
            pass
        await app.send_response(await ToVkApiMapper.convert(result), message)
