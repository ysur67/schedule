from typing import Optional

from apps.feedback.models import MessengerModel


def get_messenger_by_code(code: str) -> Optional[MessengerModel]:
    result = MessengerModel.objects.filter(code__iexact=code).first()
    if not result:
        raise ValueError(f"There is no messenger with code: {code}")
    return result
