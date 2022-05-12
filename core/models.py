from django.db import models
from django.core import validators
from djmoney.models.fields import MoneyField

import datetime


class CommonAbstractModel(models.Model):
    '''Generic class for models with the same fields.'''
    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    class Meta:
        abstract = True


class Promotion(CommonAbstractModel):
    '''Promotions in car dealerships and suppliers valid for cars.'''
    discount = models.PositiveIntegerField(validators=[validators.MaxValueValidator(50)], default=0)
    description = models.TextField(blank=True, verbose_name='Discount description')
    start = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Start discount date')
    end = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(days=3)),
                               verbose_name='End discount date')

    class Meta:
        abstract = True
