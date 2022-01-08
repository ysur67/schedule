from typing import Optional
from apps.feedback.models import MessengerModel


def get_messenger_by_code(code: str) -> Optional[MessengerModel]:
    return MessengerModel.objects.filter(code__iexact=code).first()
