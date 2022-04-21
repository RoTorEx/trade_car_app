from django.db import models
from djmoney.models.fields import MoneyField
from core.models import CommonAbstractModel


class Car(CommonAbstractModel):
    '''Brands and models of cars.'''
    car_brand = models.CharField(max_length=255, verbose_name='Car brand')
    car_model = models.CharField(max_length=255, verbose_name='Car model')

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"


class CarPrice(models.Model):
    '''The price of cars by suppliers and dealerships.'''
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Car')
    car_price = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='USD', verbose_name='Price')


class CarCharacters(models.Model):
    '''Characteristics of cars.'''
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    engine_type = models.CharField(max_length=255, verbose_name='Engine type')
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Engine capacity')
    color = models.CharField(max_length=255)
