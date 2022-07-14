from abc import ABC, abstractmethod

from apps.feedback.bots.utils.response.message import SingleMessage


class BaseResponse(ABC):

    @abstractmethod
    def to_vk_api(self, data: 'list[SingleMessage]') -> 'list[str]':
        pass
