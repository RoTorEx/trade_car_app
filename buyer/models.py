from django.db import models
from djmoney.models.fields import MoneyField


class Buyer(models.Model):
    '''Покупатели.'''
    first_name = models.CharField(max_length=255)  # Имя
    last_name = models.CharField(max_length=255)  # Фамилия
    email_address = models.CharField(max_length=255)  # Почта
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')  # Баланс

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BuyerHistory(models.Model):
    '''История купленных автомобилей покупателями.'''
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)  # Связь к покупателю
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)  # Связь к модели авто
    buy_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')  # Цена покупки

    is_active = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)  # Создание
    time_update = models.DateTimeField(auto_now=True)  # Обновление
