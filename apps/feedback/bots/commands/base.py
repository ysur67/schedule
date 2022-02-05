from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Union

from asgiref.sync import sync_to_async

from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.keyboard.base import BaseKeyboard
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.profile import \
    get_profile_by_messenger_and_account_id


@dataclass
class SingleMessage:
    message: str
    keyboard: Optional[BaseKeyboard]= None

    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "keyboard": self.keyboard
        }


@dataclass
class MultipleMessages:
    messages: Iterable[SingleMessage]


class BaseCommand(ABC):
    type: Messengers

    def __init__(self, messenger: Messengers = Messengers.VK, **kwargs) -> None:
        self.type = messenger
        self.kwargs = kwargs

    async def execute(self) -> Union[SingleMessage, MultipleMessages]:
        await self.pre_execute()
        if self.type in (Messengers.VK, Messengers.TELEGRAM):
            return await self._execute_for_messengers()
        raise NotImplementedError(f"There is no approach for type {self.type}")

    @abstractmethod
    async def _execute_for_messengers(self) -> Union[SingleMessage, MultipleMessages]:
        pass

    async def pre_execute(self) -> None:
        pass

    def _require_field(self, key: str, raise_exception: bool = True) -> Any:
        result = self.kwargs.get(key, None)
        if result is not None:
            return result
        if raise_exception:
            raise ValueError(f"You should provide {key} kwarg for this command")
        return result


class CommandWithProfile(BaseCommand):

    @property
    def account_id(self) -> str:
        return self._require_field("account_id")

    async def pre_execute(self) -> None:
        self.messenger = await sync_to_async(get_messenger_by_code)(self.type.value)
        self.profile = await sync_to_async(
            get_profile_by_messenger_and_account_id
        )(self.messenger, self.account_id)
