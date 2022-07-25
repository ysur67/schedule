from dataclasses import dataclass
from typing import Any, Optional

from apps.feedback.bots.utils.keyboard.base import SimpleKeyboard


@dataclass
class SingleMessage:
    message: str
    keyboard: Optional[SimpleKeyboard] = None

    def to_dict(self) -> 'dict[str, Any]':
        return {
            "message": self.message,
            "keyboard": self.keyboard
        }
