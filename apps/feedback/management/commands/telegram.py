from typing import Any, Optional
from django.core.management import BaseCommand
from apps.main.usecases import get_settings
from apps.feedback.bots.telegram import TelegramBot


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        settings = get_settings()
        bot = TelegramBot(settings.telegram_token)
        bot.listen()
