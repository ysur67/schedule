from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.account_messenger import create_account, get_account_by_messenger_and_id
from apps.feedback.models import MessengerAccount
from apps.feedback.usecases.profile import create_profile


class CreateAccountMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: Message, data: dict):
        messenger = await sync_to_async(get_messenger_by_code)("telegram")
        account: MessengerAccount = await sync_to_async(get_account_by_messenger_and_id)(messenger, message.from_user.id)
        if account is None:
            account = await sync_to_async(create_account)(account_id=message.from_user.id, messenger=messenger)
        # При вызове поля ForeignKey поднимается
        # джанговское исключение SynchronousOnlyOperation
        # Поэтому приходится крутить вот такой уродск, чтобы это работало
        profile = await sync_to_async(account.get_profile)()
        if profile is None:
            user = message.from_user
            fullname = f"{user.username}"
            profile = await sync_to_async(create_profile)(title=fullname)
            await sync_to_async(account.set_profile)(profile)
