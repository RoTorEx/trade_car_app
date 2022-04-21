from django.db import models
from djmoney.models.fields import MoneyField


class CommonAbstractModel(models.Model):
    '''Generic class for models with the same fields.'''
    is_active = models.BooleanField(default=True, verbose_name='Active')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time update')

    class Meta:
        abstract = True


class Offer(CommonAbstractModel):
    '''Offer to buy dealership's car.'''
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE, related_name='offer', verbose_name='Buyer')
    max_price = MoneyField(max_digits=9, decimal_places=2, null=True, default_currency='USD', verbose_name='Max price')
    car = models.ForeignKey('car.Car', on_delete=models.CASCADE, related_name='car_offer', verbose_name='Preffer car')

    def __str__(self):
        return f"{self.buyer} {self.max_price} {self.car}"


class Promotion(CommonAbstractModel):
    '''Promotions in car dealerships and suppliers valid for cars.'''
    car = models.ManyToManyField('car.Car', related_name='car_promo', verbose_name='Promo car')
    discount = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Discount')
    description = models.TextField(blank=True, verbose_name='Discount description')
    start = models.DateField(verbose_name='Start discount date')
    end = models.DateField(verbose_name='End discount date')

    dealership = models.ForeignKey(
        'dealership.Dealership',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='dealership_promos',
        verbose_name='Dealership discounts')  # Dealership

    supplier = models.ForeignKey(
        'supplier.Supplier',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='supplier_promos',
        verbose_name='Supplier discounts')  # Supplier

    def __str__(self):
        return f"{self.car} {self.discount} starts: {self.start} ends: {self.end}"
