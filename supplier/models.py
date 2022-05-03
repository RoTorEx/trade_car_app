from django.db import models
from djmoney.models.fields import MoneyField

from car.models import Car
from core.models import CommonAbstractModel, Promotion
from user.models import UserProfile


class Supplier(CommonAbstractModel):
    '''Car suppliers.'''
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='supplier_profile')
    name = models.CharField(max_length=255, verbose_name='Supplier name')
    year_of_foundation = models.DateField(verbose_name='Year of foundation')

    def __str__(self):
        return f"{self.name} {self.year_of_foundation} <{self.user}>"


class SupplierGarage(models.Model):
    '''Supplier's garage.'''
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')

    def __str__(self):
        return f"{self.car}"


class SupplierPromo(Promotion):
    '''Supplier's promotions.'''
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(SupplierGarage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.supplier} sells the {self.car} with {self.discount}% discount!"
