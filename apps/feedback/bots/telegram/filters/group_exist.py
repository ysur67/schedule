from aiogram.dispatcher.filters.filters import Filter
from asgiref.sync import sync_to_async
from apps.timetables.usecases.group import get_group_by_title
from aiogram.types import Message


class GroupExistFilter(Filter):

    async def check(self, obj: Message) -> bool:
        query = sync_to_async(get_group_by_title)
        return await query(obj.text) is not None
