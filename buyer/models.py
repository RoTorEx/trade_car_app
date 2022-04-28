from django.db import models
from djmoney.models.fields import MoneyField
from core.models import CommonAbstractModel
from user.models import UserProfile


class Buyer(CommonAbstractModel):
    '''Buyers.'''
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BuyerHistory(CommonAbstractModel):
    '''History of purchased buyers cars.'''
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)
    buy_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Purchase price')
