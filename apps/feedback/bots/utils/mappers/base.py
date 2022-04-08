from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Union

from apps.feedback.bots.commands.base import SingleMessage


class BaseMessengerMapper(ABC):

    @classmethod
    @abstractmethod
    async def convert(cls, response: Iterable[SingleMessage]) -> List[Dict]:
        """Method for converting app-wide messages
        to kwargs for api specific methods

        Returns:
            Dict: Result of mapping
        """
