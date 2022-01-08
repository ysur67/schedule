from typing import Optional
from apps.feedback.models import MessengerAccount, Profile


def get_profile_by_messenger_account(account: MessengerAccount) -> Optional[Profile]:
    return Profile.objects.filter(
        messenger_accounts__account_id=account.account_id
    ).first()


def create_profile(**options) -> Profile:
    return Profile.objects.create(**options)
