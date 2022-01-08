from typing import Union

from apps.feedback.usecases.profile import get_profile_by_account_id
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async
from apps.timetables.usecases.group import get_group_by_title


class SaveCurrentGroupCommand(BaseCommand):

    @property
    def group(self) -> str:
        return self._require_field("group")

    @property
    def account_id(self) -> str:
        return self._require_field("account_id")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        group = await sync_to_async(get_group_by_title)(self.group)
        profile = await sync_to_async(get_profile_by_account_id)(self.account_id)
        await sync_to_async(profile.set_group)(group)
        return SingleMessage(message="Ваш выбор группы был успешно сохранен")
