from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel
from core.enums import Engine, Transmission, Color


class Car(CommonAbstractModel):
    '''Cars.'''
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    engine_type = models.CharField(max_length=25, choices=Engine.choices(), verbose_name='Engine type')
    transmission = models.CharField(max_length=25, choices=Transmission.choices(), verbose_name='Transmission type')
    color = models.CharField(max_length=25, choices=Color.choices(), verbose_name='Color')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model} [{self.engine_type}, {self.transmission}, {self.color}]"
