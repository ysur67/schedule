from asgiref.sync import sync_to_async
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from apps.feedback.models import MessengerAccount
from apps.feedback.usecases.account_messenger import (
    create_account, get_account_by_messenger_and_id)
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.profile import create_profile


class CreateAccountMiddleware(BaseMiddleware[Message]):

    async def pre(self):
        messenger = await sync_to_async(get_messenger_by_code)("vk")
        account: MessengerAccount = await sync_to_async(get_account_by_messenger_and_id)(messenger, self.event.peer_id)
        if account is None:
            account = await sync_to_async(create_account)(account_id=self.event.peer_id, messenger=messenger)
        # При вызове поля ForeignKey поднимается
        # джанговское исключение SynchronousOnlyOperation
        # Поэтому приходится крутить вот такой уродск, чтобы это работало
        profile = await sync_to_async(account.get_profile)()
        if profile is None:
            user = await self.event.get_user()
            fullname = f"{user.first_name} {user.last_name}"
            profile = await sync_to_async(create_profile)(title=fullname)
            await sync_to_async(account.set_profile)(profile)
