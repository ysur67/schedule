from vkbottle import BaseMiddleware
from vkbottle.bot import Message
from apps.feedback.usecase.messenger import get_messenger_by_code
from apps.feedback.usecase.account_messenger import create_account, get_account_by_messenger_and_id
from asgiref.sync import sync_to_async


class CreateAccountMiddleware(BaseMiddleware[Message]):

    async def pre(self):
        messenger = await sync_to_async(get_messenger_by_code)("vk")
        account = await sync_to_async(get_account_by_messenger_and_id)(messenger, self.event.peer_id)
        if account is None:
            _ = await sync_to_async(create_account)(account_id=self.event.peer_id, messenger=messenger)
