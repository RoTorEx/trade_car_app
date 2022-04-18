from django.db import models
from djmoney.models.fields import MoneyField


class Buyer(models.Model):
    '''Покупатели.'''
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    email_address = models.CharField(max_length=255, verbose_name='Email address')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Buyers"


class BuyerHistory(models.Model):
    '''История купленных автомобилей покупателями.'''
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)
    buy_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Purchase price')

    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    class Meta:
        verbose_name_plural = "Buyers history"
