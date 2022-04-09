from apps.feedback.bots.commands.get_main_menu import GetMainMenuCommand
from apps.feedback.bots.commands.show_id import ShowIDCommand
from apps.feedback.bots.utils.mappers.vk import ToVkApiMapper
from apps.feedback.bots.vk.base import VkBotMixin
from vkbottle.bot import Message


def init_endpoints(app: VkBotMixin):
    @app.bot.on.message(text=["Привет", "Покажи мой ID"])
    async def echo(message: Message):
        result = await ShowIDCommand(user_id=message.peer_id).execute()
        await app.send_response(await ToVkApiMapper.convert(result), message)

    @app.bot.on.message(text=["Начать", "Главное меню"])
    async def get_main_menu(message: Message):
        result = await GetMainMenuCommand().execute()
        inline_messages = message.state_peer.payload.get('messages', None)
        if inline_messages:
            await app.bot.api.messages.delete(
                message_ids=inline_messages,
                delete_for_all=True
            )
        # TODO: custom state dispenser
        try:
            await app.bot.state_dispenser.delete(message.peer_id)
        except KeyError:
            pass
        await app.send_response(await ToVkApiMapper.convert(result), message)
