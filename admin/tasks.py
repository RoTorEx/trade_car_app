from time import sleep
from decimal import Decimal
import random as r

from admin.celery import app
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo
from supplier.models import SupplierGarage, SupplierPromo
from buyer.models import Buyer, BuyerHistory, BuyerOffer
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

    print("Start 'dealership_buy_car' task.")

    for dealer in Dealership.objects.all():
        '''Filtering suppliers' car for dealership characters.'''
        preferred_cars = SupplierGarage.objects.select_related('car').filter(
            car__car_brand__in=dealer.car_characters['car_brand'],
            car__car_model__in=dealer.car_characters['car_model'],
            car__engine_type__in=dealer.car_characters['engine_type'],
            car__transmission__in=dealer.car_characters['transmission'],
            car__color__in=dealer.car_characters['color'],
        )

        if preferred_cars:
            '''Choice one random car from preferred list.'''
            random_car = r.choice(preferred_cars)

            '''Looking for supplier car with price.'''
            supplier_car_price = SupplierGarage.objects.filter(car=random_car.car)

            '''Count of preffered supplier's cars.'''
            if supplier_car_price:
                preferred_prices = {}
                finish_tuple = tuple()

                for sup_car in supplier_car_price:  # Loop for QuerySet
                    cars_count = DealershipBuyHistory.objects.filter(
                        supplier=sup_car.supplier,
                        dealership=dealer
                    ).count()

                    preferred_prices[sup_car.supplier.id] = [sup_car, cars_count]

                '''Looking up for positive promotions.'''
                cars_promos = SupplierPromo.objects.filter(car=random_car)

                if cars_promos:
                    for car_to_promo in cars_promos:
                        preferred_prices[car_to_promo.supplier.id].append(car_to_promo.discount)

                    '''Calculate discount of car count.'''
                    # Value discount depending on the number of delivered cars, every (5) cars gives (1)% discount
                    count = int(car_to_promo.supplier.car_count)
                    count_discount = count // 5

                    # Max discount (20%) depending on the number of delivered cars
                    if count_discount > 20:
                        count_discount = 20

                else:
                    count_discount = 0

                '''Calculate discount.
                Based on the cost,
                discounts for a specific cars, if it is available,
                and discounts from sold cars.'''
                for sup_id, lst in preferred_prices.items():

                    if len(lst) == 2:  # if random car-promo IS NOT available
                        finish_tuple = (lst[0], (
                            lst[0].price.amount * Decimal(str((100 - count_discount) / 100))
                        ).quantize(Decimal('1.00')))

                    elif len(lst) == 3:  # if random car-promo IS available
                        finish_tuple = (lst[0], (
                            lst[0].price.amount * Decimal(str((100 - lst[2] - count_discount) / 100))
                        ).quantize(Decimal('1.00')))

                '''Dealership buying a car.'''
                current_car = finish_tuple[0]
                current_price = finish_tuple[1]
                current_count = r.randint(1, 10)
                # Generate random price margin to buyed car to dealership garage.
                current_new_price = (current_price * Decimal(
                    Decimal(str(r.uniform(1, 3))).quantize(Decimal('1.00'))
                )).quantize(Decimal('1.00'))

                # Check dealership balance
                if dealer.balance.amount >= current_price * current_count:

                    # Check car to enter in dealership's garage
                    current_dealer_garage = [car.car for car in
                                             DealershipGarage.objects.filter(dealership=dealer)]
                    if current_car not in current_dealer_garage:
                        DealershipGarage.objects.create(
                            car=current_car,
                            dealership=dealer,
                            car_count=current_count,
                            price=current_new_price,
                        )

                        '''Make dealer promotion to new buyed car with 33% chance.'''
                        if r.choice([True, False, False]):
                            DealershipPromo.objects.create(
                                dealership=dealer,
                                car=DealershipGarage.objects.latest('id'),
                                discount=r.randint(1, 10),
                            )

                    else:  # Updating an existing field
                        update_dealer_car = DealershipGarage.objects.filter(car=current_car,
                                                                            dealership=dealer).get()
                        update_dealer_car.car_count += current_count
                        update_dealer_car.save()

                    '''Update count of sold supplier's cars.'''
                    current_car.supplier.car_count += current_count
                    current_car.supplier.save()

                else:
                    pennies = Decimal(str(r.uniform(100_000, 800_000))).quantize(Decimal('1.00'))
                    print(f"{dealer} don't have enouth money to buy [{current_count}] {current_car}")
                    print(f"Gives some pennies [{pennies}] to him.")
                    dealer.balance.amount += pennies
                    dealer.save()

                '''Update dealer's balance.'''
                dealer.balance.amount -= current_price * current_count
                dealer.save()

                '''Writing dealership's buy history.'''
                DealershipBuyHistory.objects.create(
                    car=current_car,
                    supplier=current_car.supplier,
                    dealership=dealer,
                    price=current_price,
                    car_count=current_count,
                    common=current_price * current_count,
                )


@app.task
def create_buyer_offer(offers_num):
    '''Create random buyer's offers.'''

    print(f"Start 'create_buyer_offer' task with {offers_num} offers.")

    for _ in range(offers_num):  # Create {offers_num} random buyer's offers
        '''Random buyer make offer to buy a car from dealership.'''

        random_buyer = r.choice(Buyer.objects.all())

        '''Check for verified email.'''
        if random_buyer.user.verifyed_email:
            # Count of random: brand, engine, trasmission, color
            buyer_characters = create_characters(brd=5, eng=3, trn=3, clr=8)  # *Buyer preferences

            '''Check that preferred sum couldn't be bigger than buyer balance.'''
            max_buyer_price = Decimal(
                str(r.uniform(1_000, int(random_buyer.balance.amount)))
            ).quantize(Decimal('1.00'))

            '''Create offer to buy car.'''
            BuyerOffer.objects.create(
                buyer=random_buyer,
                max_price=max_buyer_price,
                preferred_car_characters={
                    'car_brand': buyer_characters['car_brand'],
                    'car_model': buyer_characters['car_model'],
                    'engine_type': buyer_characters['engine'],
                    'transmission': buyer_characters['transmission'],
                    'color': buyer_characters['color'],
                },
            )

        else:
            print(f"{random_buyer} must to confirm his email, before he can create car-offer!")
            continue


@app.task
def check_buyers_offer():
    '''Looking for open buyer's offers.'''

    print("Start 'check_buyers_offer' task")

    for offer in BuyerOffer.objects.exclude(active_status='close'):
        car_buyer = offer.buyer

        suit_dealers_list = DealershipGarage.objects.select_related('car').filter(
            car__car__car_brand__in=offer.preferred_car_characters['car_brand'],
            car__car__car_model__in=offer.preferred_car_characters['car_model'],
            car__car__engine_type__in=offer.preferred_car_characters['engine_type'],
            car__car__transmission__in=offer.preferred_car_characters['transmission'],
            car__car__color__in=offer.preferred_car_characters['color'],
        )

        '''Checking for best price.'''
        if not suit_dealers_list:  # suit_dealers_list == None
            pennies = Decimal(str(r.uniform(1_488, 15_000))).quantize(Decimal('1.00'))

            print(f"{car_buyer} create zero offer with max car price {offer}. Gives some pennies [{pennies}] to buyer.")

            car_buyer.balance.amount += pennies
            car_buyer.save()

        else:  # suit_dealers_list != None
            preferred_prices = {}

            for suit_dealer in suit_dealers_list:  # Dealer garage loop
                preferred_prices[suit_dealer.dealership] = [suit_dealer, suit_dealer.price.amount]
                promo_car = DealershipPromo.objects.filter(dealership=suit_dealer.dealership,
                                                           car=suit_dealer).first()

                if promo_car:  # Car discount check
                    preferred_prices[suit_dealer.dealership].append(promo_car.discount)

            for deal, lst in preferred_prices.items():
                if len(lst) == 3:
                    preferred_prices[deal].append((
                        lst[1] * Decimal(str((100 - lst[2]) / 100))).quantize(Decimal('1.00')))

            '''Find minimal preferred car cost.'''
            finish_list = []
            for deal, lst in preferred_prices.items():
                finish_list.append([deal, lst[0], lst[-1]])

            if finish_list:
                finish_list = min(finish_list, key=lambda ord: ord[-1])  # get car with minimal price

                current_dealer = finish_list[0]
                current_car = finish_list[1]
                current_price = finish_list[2]

            '''Buyer buying car.'''
            BuyerHistory.objects.create(
                buyer=car_buyer,
                car=current_car,  # ! Check!
                price=current_price
            )

            '''Check history to enter buyers inside.'''
            if not DealershipSaleHistory.objects.filter(dealership=current_dealer, buyer=car_buyer).first():
                '''Write history.'''
                DealershipSaleHistory.objects.create(
                    car=current_car,
                    dealership=current_dealer,
                    buyer=car_buyer,
                    price=current_price,
                    car_count=1,
                    total_sum=current_price,
                )

            else:
                '''Upadate history.'''
                update_buyer_car = DealershipSaleHistory.objects.filter(dealership=current_dealer,
                                                                        buyer=car_buyer).get()
                update_buyer_car.car_count += 1
                update_buyer_car.total_sum.amount += current_price
                update_buyer_car.save()

            '''Update buyer and dealership balances and count of dealership's cars.'''
            car_buyer.balance.amount -= current_price
            car_buyer.save()

            current_dealer.balance.amount += current_price
            current_dealer.save()

            current_car.car_count -= 1
            current_car.save()

            if current_car.car_count == 0:
                DealershipGarage.objects.filter(car=current_car.car, dealership=current_dealer).delete()
                print(f"Removing field from {current_car} with zero car count...")

            '''Change current offer status'''
            print(f"{offer} closed success!")
            offer.active_status = 'close'
            offer.save()
