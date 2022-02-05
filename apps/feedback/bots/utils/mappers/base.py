from abc import ABC, abstractmethod
from typing import Dict, Union
from apps.feedback.bots.commands.base import SingleMessage, MultipleMessages



class BaseMessengerMapper(ABC):

    @abstractmethod
    @classmethod
    def convert(cls, response: Union[SingleMessage, MultipleMessages]) -> Dict:
        """Method for converting app-wide messages
        to kwargs for api specific methods

        Returns:
            Dict: Result of mapping
        """
