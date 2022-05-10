from time import sleep
from faker import Faker
from decimal import Decimal
import random as r

from admin.celery import app
from user.models import UserProfile
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory
from supplier.models import Supplier, SupplierGarage
from buyer.models import Buyer, BuyerHistory
from core.models import BuyerOffer
from core.management.commands.fill_db import create_characters


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
def delete_offers():
    '''Delete buyer's offers, if they are still for a long time.'''
    print("Cleaning up all buyer's offers.")
    BuyerOffer.objects.all().delete()


@app.task
def dealership_buy_car():
    '''Random buy orders by car characteristics from a supplier.'''
    print("Start dealership_buy_carr task")

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
                pittance = Decimal(str(r.uniform(15_000, 300_000))).quantize(Decimal('1.00'))
                dealer.balance.amount += pittance
                dealer.save()
                print(f'''{dealer} don't have enouth money to buy {cnt} {random_car.car}.
                      Give some pittances ({pittance}) to his balance...''')
                continue


@app.task
def dealership_sale_car():
    '''Buyer's orders to buy car from dealership.'''
    print("Start dealership_sale_car task")

    '''Creating offer to buy car for all buyers.'''
    for car_buyer in Buyer.objects.all():

        # Count of random: brand, engine, trasmission, color
        characters_dict = create_characters(brd=5, eng=3, trn=3, clr=8)  # *Buyer preferences

        '''Check for verified email.'''
        if car_buyer.user.verifyed_email:
            max_buyer_car_price = Decimal(
                str(r.uniform(1_000, int(car_buyer.balance.amount)))
            ).quantize(Decimal('1.00'))

            '''Create offer to buy car.'''
            BuyerOffer.objects.create(
                buyer=car_buyer,
                max_price=max_buyer_car_price,
                preferred_car_characters={
                    'car_brand': characters_dict['car_brand'],
                    'car_model': characters_dict['car_model'],
                    'engine_type': characters_dict['engine'],
                    'transmission': characters_dict['transmission'],
                    'color': characters_dict['color'],
                }
            )

        else:
            # print(f"{car_buyer} email is not verified!")
            continue

        '''Looking for dealership which have preferred to buyer car.'''
        offer = BuyerOffer.objects.latest('id')
        suit_dealerships_list = DealershipGarage.objects.select_related('car').filter(
            car__car__car_brand__in=offer.preferred_car_characters['car_brand'],
            car__car__car_model__in=offer.preferred_car_characters['car_model'],
            car__car__engine_type__in=offer.preferred_car_characters['engine_type'],
            car__car__transmission__in=offer.preferred_car_characters['transmission'],
            car__car__color__in=offer.preferred_car_characters['color'],
        )

        '''Check for existence dealership with preferred list.'''
        if suit_dealerships_list:
            current_dealer_garage = suit_dealerships_list.order_by('price').first()
            buyer_balance = offer.buyer.balance
            selling_price = current_dealer_garage.price

            '''Check for deal positive Buyer balance.'''
            if buyer_balance.amount >= max_buyer_car_price >= selling_price.amount:

                '''Write success offer in the buyer history.'''
                BuyerHistory.objects.create(
                    buyer=offer.buyer,
                    car=current_dealer_garage,
                    price=selling_price.amount,
                )

                '''Write success offer in the dealership history.'''
                DealershipSaleHistory.objects.create(
                    car=current_dealer_garage,
                    dealership=current_dealer_garage.dealership,
                    buyer=offer.buyer,
                    price=selling_price.amount,
                )

                '''Update buyer and dealership balance.'''
                buyer_balance.amount -= selling_price.amount
                current_dealer_garage.dealership.balance.amount += selling_price.amount
                offer.buyer.save()
                current_dealer_garage.dealership.save()

                print(f"{offer} was success closed! Сongratulations to the buyer on his new car!")
                print("Delete used offer...")
                offer.delete()

    print("Cleaning up all buyer's offers.")
    BuyerOffer.objects.all().delete()
