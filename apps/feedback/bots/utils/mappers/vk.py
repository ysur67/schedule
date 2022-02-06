from functools import singledispatchmethod
from typing import Dict, List, Union

from asgiref.sync import sync_to_async

from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper


class ToVkApiMapper(BaseMessengerMapper):

    @singledispatchmethod
    @classmethod
    async def convert(cls, response: Union[SingleMessage, MultipleMessages]) -> Union[Dict, List[Dict]]:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

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

    @convert.register(MultipleMessages)
    @classmethod
    async def _(cls, response: MultipleMessages) -> Dict:
        return [await cls.convert(item) for item in response.messages]
