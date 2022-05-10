from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel


engine = (('gas', 'Gas'), ('diesel', 'Diesel'), ('electric', 'Electric'))

trans = (('AT', 'Automatic Transmission'), ('MT', 'Manual Transmission'), ('AM', 'Automated Manual Transmission'))

horse_power = (('<100', '<100'), ('>100', '>100'), ('>200', '>200'), ('>300', '>300'), ('>400', '>400'))

color = (('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('blue', 'Blue'), ('pink', 'Pink'),
         ('grey', 'Grey'), ('orange', 'Orange'), ('gold', 'Gold'), ('silver', 'Silver'), ('black', 'Black'))


class Car(CommonAbstractModel):
    '''Cars.'''
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    engine_type = models.CharField(max_length=25, choices=engine, verbose_name='Engine type')
    transmission = models.CharField(max_length=25, choices=trans, verbose_name='Transmission type')
    color = models.CharField(max_length=25, choices=color, verbose_name='Color')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model} [{self.engine_type}, {self.transmission}, {self.color}]"
