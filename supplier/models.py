from django.db import models
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel, Promotion


class Supplier(CommonAbstractModel):
    '''Car suppliers.'''
    user = models.OneToOneField('user.UserProfile', on_delete=models.CASCADE, related_name='supplier_profile')
    name = models.CharField(max_length=255, verbose_name='Supplier name')
    year_of_foundation = models.DateField(verbose_name='Year of foundation')

    def __str__(self):
        return f"{self.name}"


class SupplierGarage(models.Model):
    '''Supplier's garage.'''
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')

    def __str__(self):
        return f":{self.supplier}: {self.car}"


class SupplierPromo(Promotion):
    '''Supplier's promotions.'''
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    car = models.ForeignKey('supplier.SupplierGarage', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.supplier} sells the {self.car} with {self.discount}% discount!"
