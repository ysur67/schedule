from typing import Optional
from apps.feedback.models import MessengerAccount, MessengerModel, Profile
from apps.feedback.usecases.account_messenger import get_account_by_messenger_and_id


def get_profile_by_messenger_account(account: MessengerAccount) -> Optional[Profile]:
    return Profile.objects.filter(
        messenger_accounts__account_id=account.account_id
    ).first()


def get_profile_by_account_id(id: str) -> Optional[Profile]:
    return Profile.objects.filter(messenger_accounts__account_id=id).first()


def get_profile_by_messenger_and_account_id(messenger: MessengerModel, id: str) -> Optional[Profile]:
    account = get_account_by_messenger_and_id(messenger, id)
    return get_profile_by_messenger_account(account)


def create_profile(**options) -> Profile:
    return Profile.objects.create(**options)
