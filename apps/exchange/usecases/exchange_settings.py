from typing import Optional
from apps.exchange.models import ExchangeSettings


def get_exchange_settings() -> Optional[ExchangeSettings]:
    return ExchangeSettings.objects.first()
