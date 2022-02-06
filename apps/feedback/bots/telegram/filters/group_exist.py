from typing import Union

from aiogram.dispatcher.filters.filters import Filter
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from apps.timetables.usecases.group import get_group_by_title


class GroupExistFilter(Filter):

    async def check(self, obj: Union[Message, CallbackQuery]) -> bool:
        query = sync_to_async(get_group_by_title)
        if isinstance(obj, Message):
            return await query(obj.text) is not None
        return await query(obj.data) is not None
