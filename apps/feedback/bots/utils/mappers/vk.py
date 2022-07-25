from typing import Dict, Iterable, List

from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from apps.feedback.bots.utils.response.message import SingleMessage
from asgiref.sync import sync_to_async


class ToVkApiMapper(BaseMessengerMapper):

    @classmethod
    async def convert(cls, response: Iterable[SingleMessage]) -> List[Dict]:
        result = []
        for item in response:
            keyboard_data = None
            if item.keyboard:
                keyboard_data = await sync_to_async(item.keyboard.to_vk_api)()
            result.append({
                'message': item.message,
                'keyboard': keyboard_data
            })
        return result
