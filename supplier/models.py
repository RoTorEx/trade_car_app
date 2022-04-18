from django.db import models
from djmoney.models.fields import MoneyField


class Supplier(models.Model):
    '''Поставщики автомобилей.'''
    name = models.CharField(max_length=255)  # Название
    year_of_foundation = models.DateField()  # Год основания
    cars = models.ManyToManyField('car.Car')  # Связь к авто
    cars_price = models.ManyToManyField('car.Car')  # Связь к ценам на авто
    cars_config = models.ManyToManyField('car.Car')  # Связь к характеристикам авто

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление

    def __str__(self):
        return f"{self.name}"


class SupplierHistory(models.Model):
    '''История поставки автомобилей автосалонам.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)  # Связь к авто
    sold_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')  # Цена поставки
    count = models.IntegerField()  # Кол-во поставленных авто

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление
