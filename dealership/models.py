from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class Dealership(models.Model):
    '''Автосалоны.'''
    name = models.CharField(max_length=255, verbose_name='Dealership name')
    location = CountryField(verbose_name='Dealership location')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Balance')
    cars = models.ManyToManyField('car.Car', related_name='dealership_car', verbose_name='Dealership cars')
    cars_price = models.ManyToManyField('car.CarPrice', related_name='dealership_car_price', verbose_name='Price')
    cars_chars = models.ManyToManyField('car.CarCharacters', related_name='dealer_car_chars', verbose_name='Chars')
    buyers = models.ManyToManyField('buyer.Buyer', related_name='dealership_buyers', verbose_name='Unique buyers')

    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        verbose_name_plural = "Dealerships"


class DealershipHistory(models.Model):
    '''История продаж автомобилей.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE, verbose_name='Sold car')
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, verbose_name='Buyer')
    sold_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')
    count = models.IntegerField(verbose_name='Count of sold cars')

    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    class Meta:
        verbose_name_plural = "Dealerships history"
