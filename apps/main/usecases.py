from apps.main.models import ApplicationSettings


def get_settings() -> ApplicationSettings:
    return ApplicationSettings.objects.first()
