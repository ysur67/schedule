import os

from celery import Celery
from celery.beat import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'parse-groups-info-every-hour': {
        'task': 'apps.exchange.tasks.groups.parse_groups_info',
        'schedule': crontab(hour="*/3"),
    },
    'parse-lessons-info-every-hour': {
        'task': 'apps.exchange.tasks.lessons.parse_lessons_info',
        'schedule': crontab(minute="*/1"),
    },
}
