from time import sleep
from faker import Faker
from decimal import Decimal
import random as r

from admin.celery import app
from user.models import UserProfile
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory
from supplier.models import Supplier, SupplierGarage


@app.task
def hello():
    sleep(.2)
    print('\n' + "Welcome to the main page from Celery! :D" + '\n')


@app.task
def print_log(x, y):
    print("I'm Celery log...")
    print("I'm starts every minute with Celery Beat in Docker container.")
    print(f"It's just a number - {x ** y}.")


@app.task
def dealership_buy_car():
    '''Random buy orders by car characteristics from a supplier.'''

    dealerships = Dealership.objects.all()

    for dealer in dealerships:
        '''Filtering suppliers' car for dealership characters.'''
        preferred_cars = SupplierGarage.objects.select_related('car').filter(
            car__car_brand__in=dealer.car_characters['car_brand'],
            car__car_model__in=dealer.car_characters['car_model'],
            car__engine_type__in=dealer.car_characters['engine_type'],
            car__transmission__in=dealer.car_characters['transmission'],
            car__color__in=dealer.car_characters['color'],
        )

        if preferred_cars:
            # Choice one random car from preferred
            random_car = r.choice(preferred_cars)

            # Search for supplier car with price
            supplier_car_price = SupplierGarage.objects.filter(car=random_car.car).values_list('price')
            supp = SupplierGarage.objects.filter(car=random_car.car).get().supplier

            prc = supplier_car_price.get()[0]  # Car price
            cnt = r.randint(1, 4)  # Count of buy cars

            # Check dealership balance
            if dealer.balance.amount > prc * cnt:
                '''Buying car for dealership.'''
                DealershipGarage.objects.create(
                    car=random_car,
                    dealership=dealer,
                    count=cnt,
                    price=Decimal(float(prc) * 1.2),
                )

                '''White deal to history.'''
                DealershipBuyHistory.objects.create(
                    car=random_car,
                    supplier=supp,
                    dealership=dealer,
                    price=Decimal(float(prc) * 1.2),
                    count=cnt,
                    common=Decimal(float(prc) * 1.2 * cnt),
                )

                '''Change dealership balance after deal.'''
                dealer.balance.amount -= prc
                dealer.save()

            else:
                print(f"{dealer} don't have enouth money to buy {cnt} {random_car.car}")
                continue
