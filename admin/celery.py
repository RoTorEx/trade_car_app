import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

app = Celery('admin')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Celery Beat tasks
app.conf.beat_schedule = {
    'print_log_every_1_minute': {
        'task': 'core.tasks.print_log',
        'schedule': crontab(minute='*/1'),
        'args': (2, 8),
    },
    'user_every_1_minute': {
        'task': 'core.tasks.user',
        'schedule': crontab(minute='*/1')
    },
}
