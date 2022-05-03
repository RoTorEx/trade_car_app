from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel

type = (('gas', 'Gas'), ('diesel', 'Diesel'), ('electric', 'Electric'))

color = (('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('blue', 'Blue'), ('pink', 'Pink'),
         ('grey', 'Grey'), ('orange', 'Orange'), ('gold', 'Gold'), ('silver', 'Silver'), ('black', 'Black'))


class Car(CommonAbstractModel):
    '''Cars.'''
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    engine_type = models.CharField(max_length=25, choices=type, verbose_name='Engine type')
    power = models.PositiveSmallIntegerField(verbose_name='Engine power')
    color = models.CharField(max_length=25, choices=color, verbose_name='Color')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model} [{self.engine_type}, {self.power}, {self.color}]"
