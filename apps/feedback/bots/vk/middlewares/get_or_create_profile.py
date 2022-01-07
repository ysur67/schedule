from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class GetOrCreateProfileMiddleware(BaseMiddleware[Message]):

    async def pre(self):
        pass
