from dataclasses import dataclass
from typing import Any, Optional

from apps.feedback.bots.utils.keyboard.base import BaseKeyboard


@dataclass
class SingleMessage:
    message: str
    keyboard: Optional[BaseKeyboard] = None

    def to_dict(self) -> 'dict[str, Any]':
        return {
            "message": self.message,
            "keyboard": self.keyboard
        }
