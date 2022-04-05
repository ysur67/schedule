from typing import Dict, Iterable, List, Union

from apps.feedback.bots.commands.base import SingleMessage
from apps.feedback.bots.utils import keyboard
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from asgiref.sync import sync_to_async


class ToVkApiMapper(BaseMessengerMapper):

    @classmethod
    async def convert(cls, response: Iterable[SingleMessage]) -> List[Dict]:
        result = []
        for item in response:
            keyboard_data = None
            if item.keyboard:
                keyboard_data = await sync_to_async(item.keyboard.to_vk_api)()
            if keyboard_data is None:
                result.append({
                    'message': item.message
                })
            if isinstance(keyboard_data, str):
                result.append({
                    'message': item.message,
                    'keyboard': keyboard_data
                })
            if isinstance(keyboard_data, list):
                result.append({
                    'message': item.message,
                })
                for index, elem in enumerate(keyboard_data):
                    result.append({
                        'message': f'{index + 1}.',
                        'keyboard': elem
                    })
        return result
