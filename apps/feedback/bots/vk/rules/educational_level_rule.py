from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title


class EducationalLevelExistRule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:
        query = sync_to_async(get_educational_level_by_title)
        return await query(event.text) is not None
