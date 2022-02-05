from typing import Any, Optional

from django.core.management import BaseCommand

from apps.feedback.bots.vk.bot import VkBot
from apps.main.usecases import get_settings


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        settings = get_settings()
        bot = VkBot(settings.vk_token)
        bot.listen()
