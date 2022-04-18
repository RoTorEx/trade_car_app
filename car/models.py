from django.db import models
from djmoney.models.fields import MoneyField


class Car(models.Model):
    '''Марки и модели автомобилей.'''
    car_brand = models.CharField(max_length=255, verbose_name='Car brand')
    car_model = models.CharField(max_length=255, verbose_name='Car model')

    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"

    class Meta:
        verbose_name_plural = "Cars"


class CarPrice(models.Model):
    '''Цена автомобилей по поставщикам и салонам.'''
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Car')
    car_price = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='USD', verbose_name='Price')

    class Meta:
        verbose_name_plural = "Cars price"


class СarCharacters(models.Model):
    '''Характеристики автомобилей.'''
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    engine_type = models.CharField(max_length=255, verbose_name='Engine type')
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Engine capacity')
    color = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Car characters"
