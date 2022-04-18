from django.db import models
from djmoney.models.fields import MoneyField


class Car(models.Model):
    '''Марки и модели автомобилей.'''
    car_brand = models.CharField(max_length=255)  # Бренд
    car_model = models.CharField(max_length=255)  # Модель

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"


class CarPrice(models.Model):
    '''Цена автомобилей по поставщикам и салонам.'''
    car = models.ForeignKey('Car', on_delete=models.CASCADE)  # Связь к модели авто
    car_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')  # Цена


class СarConfig(models.Model):
    '''Характеристики автомобилей.'''
    car = models.OneToOneField('Car', on_delete=models.CASCADE,)  # Свять к модели авто
    engine_type = models.CharField(max_length=255)  # Тип двигателя
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1)  # Объём двигателя
    # fuel_consumption = models.DecimalField(max_digits=4, decimal_places=1)  # Расход топлива
    color = models.CharField(max_length=255)  # Цвет авто
