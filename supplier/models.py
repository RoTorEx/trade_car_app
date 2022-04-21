from django.db import models
from djmoney.models.fields import MoneyField
from core.models import CommonAbstractModel


class Supplier(CommonAbstractModel):
    '''Car suppliers.'''
    name = models.CharField(max_length=255, verbose_name='Supplier name')
    year_of_foundation = models.DateField(verbose_name='Year of foundation')
    cars = models.ManyToManyField('car.Car', related_name='supplier_car', verbose_name='Supplier cars')
    cars_price = models.ManyToManyField('car.CarPrice', related_name='supplier_car_price', verbose_name='Price')
    cars_chars = models.ManyToManyField('car.CarCharacters', related_name='supplier_car_chars', verbose_name='Chars')

    def __str__(self):
        return f"{self.name}"


class SupplierHistory(CommonAbstractModel):
    '''History of deliveries to car dealerships.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)
    sold_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')
    count = models.IntegerField(verbose_name='Count of supplied cars')
