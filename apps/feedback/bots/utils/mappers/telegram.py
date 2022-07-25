from typing import Dict, Iterable

from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from apps.feedback.bots.utils.response.message import SingleMessage
from asgiref.sync import sync_to_async


class ToTelegramApiMapper(BaseMessengerMapper):

    @classmethod
    async def convert(cls, response: Iterable[SingleMessage]) -> Iterable[Dict]:
        result = []
        for item in response:
            keyboard_data = None
            if item.keyboard:
                keyboard_data = await sync_to_async(item.keyboard.to_telegram_api)()
            result.append({
                'text': item.message,
                'reply_markup': keyboard_data
            })
        return result
