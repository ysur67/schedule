from functools import singledispatchmethod
from typing import Dict, Union
from apps.feedback.bots.utils.mappers.base import BaseMessengerMapper
from apps.feedback.bots.commands.base import SingleMessage, MultipleMessages


class ToVkApiMapper(BaseMessengerMapper):

    @singledispatchmethod
    def convert(self, response: Union[SingleMessage, MultipleMessages]) -> Dict:
        raise NotImplementedError(f"There is no approach for type {type(response)}")

    @convert.register(SingleMessage)
    def _(self, response: SingleMessage) -> Dict:
        return {
            "message": response.message,
            "keyboard": response.keyboard.to_vk_api()
        }

    @convert.register(MultipleMessages)
    def _(self, response: MultipleMessages) -> Dict:
        return [self.convert(item) for item in response.messages]
