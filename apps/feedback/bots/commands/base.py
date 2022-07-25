from abc import ABC, abstractmethod
from typing import Any, Iterable

from apps.feedback.bots.utils.const import Messengers
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.feedback.models import MessengerModel, Profile
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.profile import \
    get_profile_by_messenger_and_account_id
from asgiref.sync import sync_to_async


class BaseCommand(ABC):
    type: Messengers

    def __init__(self, messenger: Messengers = Messengers.VK, **kwargs) -> None:
        self.type = messenger
        self.kwargs = kwargs

    async def execute(self) -> Iterable[SingleMessage]:
        await self.pre_execute()
        if self.type in (Messengers.VK, Messengers.TELEGRAM):
            return await self._execute()
        raise NotImplementedError(f"There is no approach for type {self.type}")

    @abstractmethod
    async def _execute(self) -> Iterable[SingleMessage]:
        pass

    async def pre_execute(self) -> None:
        pass

    def _require_field(self, key: str, raise_exception: bool = True) -> Any:
        result = self.kwargs.get(key, None)
        if result is not None:
            return result
        if raise_exception:
            raise ValueError(
                f"You should provide {key} kwarg for this command")
        return result


class CommandWithProfile(BaseCommand):
    profile: Profile
    messenger: MessengerModel

    @property
    def account_id(self) -> str:
        return self._require_field("account_id")

    async def pre_execute(self) -> None:
        self.messenger = await sync_to_async(get_messenger_by_code)(self.type.value)
        self.profile = await sync_to_async(
            get_profile_by_messenger_and_account_id
        )(self.messenger, self.account_id)
