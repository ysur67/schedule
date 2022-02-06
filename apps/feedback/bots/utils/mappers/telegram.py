from functools import singledispatchmethod
from typing import Dict, Union, List
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from apps.feedback.bots.commands.base import SingleMessage, MultipleMessages
from asgiref.sync import sync_to_async


class ToTelegramApiMapper(BaseMessengerMapper):

    @singledispatchmethod
    @classmethod
    async def convert(cls, response: Union[SingleMessage, MultipleMessages]) -> Union[Dict, List[Dict]]:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

    @convert.register(SingleMessage)
    @classmethod
    async def _(cls, response: SingleMessage) -> Dict:
        keyboard_data = None
        if response.keyboard:
            keyboard_data = await sync_to_async(response.keyboard.to_telegram_api)()
        return {
            "text": response.message,
            "reply_markup": keyboard_data
        }

    @convert.register(MultipleMessages)
    @classmethod
    async def _(cls, response: MultipleMessages) -> Dict:
        return [await cls.convert(item) for item in response.messages]
