from typing import Iterable, Union

from apps.feedback.bots.commands.get_main_menu import get_main_menu_layout
from apps.feedback.bots.utils.keyboard.base import SimpleKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.feedback.const import MAX_DAYS_OFFSET
from asgiref.sync import sync_to_async

from .base import CommandWithProfile


class SetDaysOffsetCommand(CommandWithProfile):

    @property
    def new_days_offset(self) -> int:
        return self._require_field("days_offset")

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = SimpleKeyboard(data=get_main_menu_layout())
        try:
            offset = int(self.new_days_offset)
        except ValueError:
            offset = None
        if not offset or offset < 1:
            result = "Ты ввел очень странный формат кол-ва дней, я его не понял...\n"
            result += f"Сейчас ты получаешь расписание на {self.profile.days_offset} дней"
            return [SingleMessage(
                message=result,
                keyboard=keyboard
            )]
        if offset > MAX_DAYS_OFFSET:
            result = "Ты ввел больше дней, чем позволяет сайт с расписанием\n"
            result += f"Сейчас ты получаешь расписание на {self.profile.days_offset} дней"
            return [SingleMessage(
                message=result,
                keyboard=keyboard
            )]
        await sync_to_async(self.profile.set_days_offset)(offset)
        msg = f"Теперь ты будешь получать расписание на {self.profile.days_offset} дней!"
        return [SingleMessage(
            message=msg,
            keyboard=keyboard
        )]
