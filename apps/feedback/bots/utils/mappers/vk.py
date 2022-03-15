from functools import singledispatchmethod
from typing import Dict, Iterable, List, Union

from apps.feedback.bots.commands.base import SingleMessage
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from asgiref.sync import sync_to_async


class ToVkApiMapper(BaseMessengerMapper):

    @singledispatchmethod
    @classmethod
    async def convert(cls, response: Iterable[SingleMessage]) -> Union[Dict, List[Dict]]:
        raise NotImplementedError(
            f"There is no approach for type {type(response)}")

    @convert.register(SingleMessage)
    @classmethod
    async def _(cls, response: SingleMessage) -> Union[Dict, List[Dict]]:
        keyboard_data = None
        if response.keyboard:
            keyboard_data = await sync_to_async(response.keyboard.to_vk_api)()
        if keyboard_data is None:
            return {
                "message": response.message
            }
        if isinstance(keyboard_data, str):
            return {
                "message": response.message,
                "keyboard": keyboard_data
            }
        elif isinstance(keyboard_data, list):
            return [{
                "message": response.message,
                "keyboard": item
            } for item in keyboard_data]

    @convert.register(list)
    @classmethod
    async def _(cls, response: 'list[SingleMessage]') -> Dict:
        return [await cls.convert(item) for item in response]
