from aiogram.dispatcher.filters.filters import Filter
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title
from aiogram.types import Message


class EducationalLevelExistFilter(Filter):

    async def check(self, obj: Message) -> bool:
        query = sync_to_async(get_educational_level_by_title)
        return await query(obj.text) is not None
