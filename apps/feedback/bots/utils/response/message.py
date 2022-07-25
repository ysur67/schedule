from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SingleMessage:
    message: str
    keyboard: Optional[Any] = None

    def to_dict(self) -> 'dict[str, Any]':
        return {
            "message": self.message,
            "keyboard": self.keyboard
        }
