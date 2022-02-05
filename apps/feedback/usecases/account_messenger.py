from typing import Optional

from apps.feedback.models import MessengerAccount, MessengerModel


def get_account_by_messenger_and_id(messenger: MessengerModel, id: str) -> Optional[MessengerAccount]:
    return MessengerAccount.objects.filter(messenger=messenger, account_id=id).first()


def create_account(**options) -> MessengerAccount:
    return MessengerAccount.objects.create(**options)
