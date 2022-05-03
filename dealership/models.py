from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from car.models import Car
from supplier.models import Supplier, SupplierGarage
from core.models import CommonAbstractModel, Promotion
from user.models import UserProfile


def get_car_characters():
    return {'car_brand': [], 'car_model': [], 'engine_type': [], 'power': [], 'color': []}


class Dealership(CommonAbstractModel):
    '''Dealership.'''
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='dealership_profile')
    name = models.CharField(max_length=255, verbose_name='Dealership name')
    location = CountryField(verbose_name='Dealership location')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Balance')
    car_characters = models.JSONField(default=get_car_characters)

    def __str__(self):
        return f"{self.name} - {self.location} <{self.user}>"


class DealershipGarage(CommonAbstractModel):
    '''Dealership's garage.'''
    car = models.ForeignKey(SupplierGarage, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')
    # selling_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')

    def __str__(self):
        return f"{self.car}"


class DealershipBuyHistory(models.Model):
    '''History of deliveries cars to dealerships.'''
    car = models.ForeignKey(SupplierGarage, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')
    count = models.PositiveIntegerField(default=1)
    common = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Total price')

    def __str__(self):
        return f'{self.supplier}: {self.dealership} -> {self.car}'


class DealershipSaleHistory(CommonAbstractModel):
    '''History of car sales.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE, verbose_name='Sold car')
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, verbose_name='Dealership')
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, verbose_name='Buyer')
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')
    count = models.IntegerField(verbose_name='Count of sold cars')

    def __str__(self):
        return f'{self.car}: {self.dealership} ({self.buyer}) - {self.price} - {self.count}'


class DealershipPromo(Promotion):
    '''Dealership's promotions.'''
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(DealershipGarage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dealership} sells the {self.car} with {self.discount}% discount!"
