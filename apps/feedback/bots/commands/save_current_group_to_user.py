from typing import Iterable

from apps.feedback.bots.commands.get_main_menu import get_main_menu_layout
from apps.feedback.bots.utils.keyboard.base import SimpleKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.timetables.usecases.group import get_group_by_title
from asgiref.sync import sync_to_async

from .base import CommandWithProfile


class SaveCurrentGroupCommand(CommandWithProfile):

    @property
    def group(self) -> str:
        return self._require_field("group")

    async def _execute(self) -> Iterable[SingleMessage]:
        group = await sync_to_async(get_group_by_title)(self.group)
        await sync_to_async(self.profile.set_group)(group)
        keyboard = SimpleKeyboard(data=get_main_menu_layout())
        return [SingleMessage(
            message="Ваш выбор группы был успешно сохранен", keyboard=keyboard
        )]
