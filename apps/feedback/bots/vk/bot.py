from vkbottle.bot import Bot, Message
from apps.feedback.bots import BaseBot


class VkBot(BaseBot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.bot = Bot(self.token)
        self.init_commands()

    def listen(self) -> None:
        self.bot.run_forever()

    def init_commands(self) -> None:
        @self.bot.on.message(text="Привет")
        async def echo(message: Message):
            await message.answer(f"Привет, {message.peer_id}")
