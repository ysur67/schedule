from typing import Union
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async
from apps.timetables.usecases.group import get_group_by_title


class SaveCurrentGroupCommand(CommandWithProfile):

    @property
    def group(self) -> str:
        return self._require_field("group")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        group = await sync_to_async(get_group_by_title)(self.group)
        await sync_to_async(self.profile.set_group)(group)
        return SingleMessage(message="Ваш выбор группы был успешно сохранен")
