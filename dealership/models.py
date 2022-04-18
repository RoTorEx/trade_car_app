from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class Dealership(models.Model):
    '''Автосалоны.'''
    name = models.CharField(max_length=150, verbose_name='name')
    location = CountryField(verbose_name='location')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='balance')
    cars = models.ManyToManyField('car.Car')  # Связь к авто
    cars_price = models.ManyToManyField('car.Car')  # Связь к ценам на авто
    cars_config = models.ManyToManyField('car.Car')  # Связь к характеристикам авто
    buyers = models.ManyToManyField('buyer.Buyer')  # Связь к уникальным покупателям

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление

    def __str__(self):
        return f"{self.name} - {self.location}"


class DealershipHistory(models.Model):
    '''История продаж автомобилей.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)  # Связь к авто
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE)  # Связь к покупателю
    sold_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')  # Цена продажи
    count = models.IntegerField()  # Кол-во проданных

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление
