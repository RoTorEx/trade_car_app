import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

app = Celery('admin')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Celery Beat tasks
app.conf.beat_schedule = {
    'dealership_buy_car_every_10_minute': {
        'task': 'core.tasks.dealership_buy_car',
        'schedule': crontab(minute='*/1'),
    },
}