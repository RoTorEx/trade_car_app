from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel
from core.enums import OfferStatus


def get_preferred_car_characters():
    return {'car_brand': [], 'car_model': [], 'engine_type': [], 'transmission': [], 'color': []}


class Buyer(CommonAbstractModel):
    '''Buyers.'''
    user = models.OneToOneField('user.UserProfile', on_delete=models.CASCADE, related_name='buyer_profile')
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BuyerHistory(models.Model):
    '''History of purchased buyers cars.'''
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.DealershipGarage', on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Purchase price')
    deal_date = models.DateTimeField(auto_now_add=True)


class BuyerOffer(CommonAbstractModel):
    '''Buyer's offer to buy dealership's car.'''
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, related_name='buyer', verbose_name='Buyer')
    max_price = MoneyField(max_digits=9, decimal_places=2, null=True, default_currency='USD', verbose_name='Max price')
    preferred_car_characters = models.JSONField(default=get_preferred_car_characters)
    active_status = models.CharField(default='open', max_length=63,
                                     choices=OfferStatus.choices(), verbose_name='Offer status')

    def __str__(self):
        return f"{self.max_price}"


class BuyerStatistic(models.Model):
    buyer_stat = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE)
    total_spent_sum = MoneyField(max_digits=9, decimal_places=2, null=True, default_currency='USD')
    total_car_count = models.PositiveIntegerField(default=0, verbose_name='Total count of sold cars')

    def __str__(self):
        return f"{self.buyer_stat} spend {self.total_spent_sum} and bought {self.total_car_count} cars."
