from django.db import models
from djmoney.models.fields import MoneyField


class Supplier(models.Model):
    '''Поставщики автомобилей.'''
    name = models.CharField(max_length=255, verbose_name='Supplier name')
    year_of_foundation = models.DateField(verbose_name='Year of foundation')
    cars = models.ManyToManyField('car.Car', related_name='supplier_car', verbose_name='Supplier cars')
    cars_price = models.ManyToManyField('car.CarPrice', related_name='supplier_car_price', verbose_name='Price')
    cars_chars = models.ManyToManyField('car.СarCharacters', related_name='supplier_car_chars', verbose_name='Chars')

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class SupplierHistory(models.Model):
    '''История поставки автомобилей автосалонам.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)
    sold_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')
    count = models.IntegerField(verbose_name='Count of supplied cars')

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
