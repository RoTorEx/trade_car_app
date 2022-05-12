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
        'task': 'admin.tasks.dealership_buy_car',
        'schedule': crontab(minute='*/10'),
    },
    'create_buyer_offer_every_5_minute': {
        'task': 'admin.tasks.create_buyer_offer',
        'schedule': crontab(minute='*/5'),
        'args': (3, ),  # count of random offers for one task
    },
    'check_buyers_offer_every_10_minute': {
        'task': 'admin.tasks.check_buyers_offer',
        'schedule': crontab(minute='*/10'),
    },
}
