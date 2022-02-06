from functools import singledispatchmethod
from typing import Dict, Union, List
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from apps.feedback.bots.commands.base import SingleMessage, MultipleMessages
from asgiref.sync import sync_to_async
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


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
        if keyboard_data is None:
            return {
                "text": response.message,
            }
        if isinstance(keyboard_data, ReplyKeyboardMarkup):
            return {
                "text": response.message,
                "reply_markup": keyboard_data
            }
        if isinstance(keyboard_data, list):
            return [{
                "text": response.message,
                "reply_markup": item
            } for item in keyboard_data]
        raise NotImplementedError(f"There is no approach for type {type(keyboard_data)}")

    @convert.register(MultipleMessages)
    @classmethod
    async def _(cls, response: MultipleMessages) -> Dict:
        return [await cls.convert(item) for item in response.messages]
