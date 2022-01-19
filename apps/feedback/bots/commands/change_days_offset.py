from typing import Union
from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.main_menu import MainMenuKeyboard
from apps.feedback.const import MAX_DAYS_OFFSET
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class SetDaysOffsetCommand(CommandWithProfile):

    @property
    def new_days_offset(self) -> int:
        return self._require_field("days_offset")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        _keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        keyboard_data = _keyboard.to_vk_api()
        try:
            offset = int(self.new_days_offset)
        except ValueError:
            offset = None
        if offset > MAX_DAYS_OFFSET:
            result = "Ты ввел больше дней, чем позволяет сайт с расписанием\n"
            result += f"Сейчас ты получаешь расписание на {self.profile.days_offset} дней"
            return SingleMessage(
                message=result,
                keyboard=keyboard_data
            )
        if not offset:
            result = "Ты ввел очень странный формат кол-ва дней, я его не понял...\n"
            result += f"Сейчас ты получаешь расписание на {self.profile.days_offset} дней"
            return SingleMessage(
                message=result,
                keyboard=keyboard_data
            )
        await sync_to_async(self.profile.set_days_offset)(offset)
        msg = f"Теперь ты будешь получать расписание на {self.profile.days_offset} дней!"
        return SingleMessage(
            message=msg,
            keyboard=keyboard_data
        )
