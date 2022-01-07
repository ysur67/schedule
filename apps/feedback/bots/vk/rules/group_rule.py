from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from asgiref.sync import sync_to_async
from apps.timetables.usecases.group import get_group_by_title


class GroupExistRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        query = sync_to_async(get_group_by_title)
        return await query(event.text) is not None
