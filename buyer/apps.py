from tabnanny import verbose
from django.apps import AppConfig


class BuyerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buyer'
    verbose_name = 'Car buyers'
