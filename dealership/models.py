from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from core.models import CommonAbstractModel, Promotion


def get_car_characters():
    return {'car_brand': [], 'car_model': [], 'engine_type': [], 'transmission': [], 'color': []}


class Dealership(CommonAbstractModel):
    '''Dealership.'''
    user = models.OneToOneField('user.UserProfile', on_delete=models.CASCADE, related_name='dealership_profile')
    name = models.CharField(max_length=255, verbose_name='Dealership name')
    location = CountryField(verbose_name='Dealership location')
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Balance')
    car_characters = models.JSONField(default=get_car_characters)

    def __str__(self):
        return f"{self.name} [{self.location}]"


class DealershipGarage(CommonAbstractModel):
    '''Dealership's garage.'''
    car = models.ForeignKey('supplier.SupplierGarage', on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_count = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')

    def __str__(self):
        return f"{self.dealership} [{self.car}: {self.price}]"


class DealershipBuyHistory(models.Model):
    '''History of deliveries cars to dealerships.'''
    car = models.ForeignKey('supplier.SupplierGarage', on_delete=models.CASCADE)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Price')
    car_count = models.PositiveIntegerField(default=1)
    common = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Total price')

    def __str__(self):
        return f'{self.supplier}: {self.car} -> {self.dealership}'


class DealershipSaleHistory(CommonAbstractModel):
    '''History of car sales.'''
    car = models.ForeignKey('dealership.DealershipGarage', on_delete=models.CASCADE, verbose_name='Sold car')
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE, verbose_name='Dealership')
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, verbose_name='Buyer')  # careful with CirleError
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Sold price')
    car_count = models.PositiveIntegerField(default=1)
    total_sum = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', verbose_name='Total sum')

    def __str__(self):
        return f'{self.car}: {self.dealership} ({self.buyer}) - {self.price} - {self.car_count}'


class DealershipPromo(Promotion):
    '''Dealership's promotions.'''
    dealership = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    car = models.ForeignKey('dealership.DealershipGarage', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dealership} sells the {self.car} with {self.discount}% discount!"


class DealerStatistic(models.Model):
    dealership_stat = models.ForeignKey('dealership.Dealership', on_delete=models.CASCADE)
    total_spent_sum = MoneyField(max_digits=9, decimal_places=2, null=True, default_currency='USD')
    total_revenue_sum = MoneyField(max_digits=9, decimal_places=2, null=True, default_currency='USD')
    total_buy_car_count = models.PositiveIntegerField(default=0)
    total_spent_car_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.dealership_stat} made {self.total_revenue_sum} $ and spent {self.total_spent_sum} $."
