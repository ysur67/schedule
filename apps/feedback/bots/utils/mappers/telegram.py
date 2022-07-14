from typing import Dict, Iterable

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
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
            if keyboard_data is None:
                result.append({
                    'text': item.message
                })
            if isinstance(keyboard_data, (InlineKeyboardMarkup, ReplyKeyboardMarkup)):
                result.append({
                    'text': item.message,
                    'reply_markup': keyboard_data
                })
            if isinstance(keyboard_data, list):
                result.append({
                    'text': item.message,
                })
                for index, elem in enumerate(keyboard_data):
                    result.append({
                        'text': f'{index + 1}.',
                        'reply_markup': elem
                    })
        return result
