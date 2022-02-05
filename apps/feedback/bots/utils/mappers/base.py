from abc import ABC, abstractmethod
from typing import Dict, Union, List
from apps.feedback.bots.commands.base import SingleMessage, MultipleMessages


class BaseMessengerMapper(ABC):

    @classmethod
    @abstractmethod
    async def convert(cls, response: Union[SingleMessage, MultipleMessages]) -> Union[Dict, List[Dict]]:
        """Method for converting app-wide messages
        to kwargs for api specific methods

        Returns:
            Dict: Result of mapping
        """
