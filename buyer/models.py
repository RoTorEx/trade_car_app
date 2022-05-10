from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel


def get_preferred_car_characters():
    return {'car_brand': [], 'car_model': [], 'engine_type': [], 'transmission': [], 'color': []}


class Buyer(CommonAbstractModel):
    '''Buyers.'''
    user = models.OneToOneField('user.UserProfile', on_delete=models.CASCADE, related_name='buyer_profile')
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user})"


class BuyerHistory(models.Model):
    '''History of purchased buyers cars.'''
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.DealershipGarage', on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Purchase price')
    deal_date = models.DateTimeField(auto_now_add=True)
