from django.core.management.base import BaseCommand
from django.db.models import Min, F
from django_countries import data as countries_data

import datetime
import time
import random as r
from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal

from user.models import UserProfile
from car.models import Car, engine, color, trans
# from core.models import BuyerOffer
from buyer.models import Buyer, BuyerHistory, BuyerOffer
from supplier.models import Supplier, SupplierGarage, SupplierPromo
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory, DealershipPromo


brand_model = {
    'McLarn': ['570S', '600LT', '720S'],
    'Aston Martin': ['DB11', 'DB9', 'DBX', 'DBX', 'V12 Vintage'],
    'Maserati': ['Levante', 'GranTurismo'],
    'Porsche': ['911', '911 GT2', '911 GT4', '928', '944', 'Macan', 'Cayman', 'Cayman GT4', 'Cayenne'],
    'Tesla': ['Model 3', 'Model S', 'Model X', 'Roadster'],
    'Volvo': ['S40', 'S60', 'S80', 'S90', 'XC40', 'XC60', 'XC80', 'SX90'],
    'Skoda': ['Fabia', 'Octavia', 'Rapid', 'Superb'],
    'Audi': ['80', '100', 'A4', 'A5', 'A7', 'RS4', 'RS5', 'RS7', 'Q5', 'Q7', 'TT', 'TT RS'],
    'BMW': ['i3', 'i5' 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'X5', 'X5 M', 'X6', 'X6 M', 'X7'],
    'Mersedes-Benz': ['190', 'W124', 'CLS,', 'GLS', 'Maybach G 650 Landaulet', 'Maybach GLS', 'Maybach S-Класс'],
    'Honda': ['Civic', 'Civic Type R', 'Integra', 'Accord', 'CR-X', 'CR-Z', 'CR-V'],
    'Mitsubishi': ['Carisma', 'Eclipse', 'Lancer Evolution', 'Sigma', ],
    'Volkswagen': ['Polo', 'Polo GTI', 'Golf', 'Gold GTI', 'Golf R', 'Passat', 'Passat CC', 'Tiguan'],
    'Mazda': ['CX-3', 'CX-5', 'CX-7', '626', '929', 'RX-7', 'RX-8', 'Roadster'],
    'Toyota': ['Supra', 'Mark II', 'Mark X' 'Camry', 'Yaris', 'Prius', 'Corolla'],
    'Nissan': ['GT-R', 'Serena', 'Almera'],
    'Subary': ['Impreza WRX', 'Impreza WRX STi', 'Legacy', 'WRX', 'Impreza', 'Forester', 'Outback'],
    'Infinity': ['Q30', 'Q50', 'Q70', 'EX', 'FX', 'G', 'I', 'J' 'QX30', 'QX50', 'QX70'],
    'MINI': ['Clubman', 'Coupe', 'Countryman', 'Cabrio', 'Paceman'],
    'Jeep': ['Grand Cherokee', 'Wrangler', 'Compass'],
    'DODGE': ['Charger', 'Challanger', 'Durando', 'Neon'],
    'OPEL': ['Astra', 'Antara', 'Insignia', 'Omega', 'Vectra', 'Corsa'],
    'Chevrolet': ['Niva', 'Tahoe', 'Cobalt', 'Camaro'],
    'Frod': ['Modeo', 'Mustang', 'Focus'],
    'Geely': ['Atlas', 'Coolray'],
    'ВАЗ': ['Granta', 'Niva', 'Vesta', 'XRAY '],
    'УАЗ': ['Hunter', '3151'],
    'ГАЗ': ['21 "Волга"', '24 "Волга"'],
    'ЗИЛ': ['130', '133'],
    'Богдан': ['2310'],
}


class Provider(BaseProvider):
    '''Extension Faker() class with dealership_list.'''
    def dealer(self):
        dealership_list = ['Борисхоф', 'Ирбис', 'ТЕХИНКОМ', 'АВТОДОМ', 'АвтоГЕРМЕС', 'АвтоЛидер', 'ЛУКАВТО',
                           'Ангар Авто', 'Авилон', 'Петровский Автоцентр', 'Resale-auto', 'РОЛЬФ Сити',
                           'FAVORIT MOTORS', 'Мас Моторс', 'Панавто', 'Major Auto', 'АвтоСпецЦентр', 'БалтАвтоТрейд-М',
                           'АванТайм', 'Агалат', 'Немецкий Дом', 'Мега Моторс', 'Автомир Богемия', 'PEGAS',
                           'Major Expert', 'Спорткар-центр', 'Автомаркет', 'ALTERA', 'АвтоГарант', 'Trade-in',
                           'ПеГас-Моторс', 'PTP-АВТО', 'Автолайт', '100 Дорог', '1001 автомобиль', 'Автобург',
                           'Автокей', 'Автомобилия', 'Автомолл', 'Германика', 'Звезды Невы', 'Каретный ряд',
                           'Машинный двор', 'МотоЛенд', 'Мультимоторс', 'Сто коней', 'Тачки тут', 'Остров',
                           'Четыре колеса', 'Колесо', '43 миля', 'Автохит', 'АвтоСтарт', 'Агат', 'Азимут Авто',
                           'Альянс', 'Альянс-Авто', 'Арго', 'Бавария', 'Балчуг', 'Викинги', 'Виктория', 'Вираж',
                           'Галерея', 'Грант Авто', 'Диалог-Авто', 'Драйв Моторс', 'Инком-Авто', 'Интеркар', 'Столица',
                           'Тысяча огней', 'Центральный', 'Флагман']
        return r.choice(dealership_list)


def create_characters(brd, eng, trn, clr):
    '''Method create random preferred car characters.'''
    car_brand = list(set([r.choice(list(brand_model.keys())) for _ in range(brd)]))
    car_model = []

    for i in car_brand:
        car_model += brand_model[i]

    car_engine = list(set([r.choice(engine)[0] for _ in range(eng)]))
    car_transmission = list(set([r.choice(trans)[0] for _ in range(trn)]))
    car_color = list(set([r.choice(color)[0] for _ in range(clr)]))

    return {'car_brand': car_brand,
            'car_model': car_model,
            'engine': car_engine,
            'transmission': car_transmission,
            'color': car_color}


def usr(usr_role, name):
    '''Role distributing method.'''
    UserProfile.objects.create(
        username=name,
        email=Faker().email(),
        password='9ol8ik7uj',
        role=usr_role,
        verifyed_email=r.choice([True, ])
    )


class Command(BaseCommand):
    help = '''Expanding the functionality of the basic app commands.'''

    def handle(self, *args, **options):

        '''Variables.'''
        count_cars = 144
        count_buyers = 16
        count_suppliers = 6
        count_dealership = 8

        '''Create superusers.'''
        if not UserProfile.objects.filter(username__in=('root', 'admin')):
            UserProfile.objects.create_superuser('root', 'root@example.com', '1234')
            UserProfile.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("===< Created superusers >===")

        '''Clear databases.'''
        UserProfile.objects.filter(is_superuser=False).delete()
        Car.objects.all().delete()

        '''Car.'''
        for _ in range(count_cars):
            car = r.choice(list(brand_model.keys()))

            Car.objects.create(
                car_brand=car,
                car_model=r.choice(brand_model[car]),
                engine_type=r.choice(engine)[0],
                transmission=r.choice(trans)[0],
                color=r.choice(color)[0],
                description=Faker().text(),
            )

        '''Staff.'''
        for i in range(12):
            usr('staff', str(i) + '_app_user')

        '''Buyer.'''
        for _ in range(count_buyers):
            usr('buyer', Faker().user_name())  # Create buyer user

            Buyer.objects.create(
                user=UserProfile.objects.latest('id'),
                first_name=Faker().first_name(),
                last_name=Faker().last_name(),
                balance=Decimal(str(r.uniform(100_000, 1_000_000))).quantize(Decimal('1.00')),
            )

        '''Supplier.'''
        for _ in range(count_suppliers):
            usr('supplier', Faker().user_name())  # Create supplier user

            Supplier.objects.create(
                user=UserProfile.objects.latest('id'),
                name=Faker().company(),
                year_of_foundation=datetime.date(r.randint(1900, 2022), r.randint(1, 12), r.randint(1, 28)),
            )

        '''Dealership.'''
        f = Faker()
        f.add_provider(Provider)  # Register custom Faker class

        for _ in range(count_dealership):
            usr('dealership', Faker().user_name())  # Create delership user

            # Count of random: brand, engine, trasmission, color
            characters_dict = create_characters(brd=5, eng=3, trn=3, clr=10)  # *Dealership preferences

            Dealership.objects.create(
                user=UserProfile.objects.latest('id'),
                name=f.dealer(),
                location=r.choice(list(countries_data.COUNTRIES.keys())),
                balance=Decimal(str(r.uniform(150_000, 3_000_000))).quantize(Decimal('1.00')),
                car_characters={
                    'car_brand': characters_dict['car_brand'],
                    'car_model': characters_dict['car_model'],
                    'engine_type': characters_dict['engine'],
                    'transmission': characters_dict['transmission'],
                    'color': characters_dict['color'],
                }
            )

        '''Supplier cars.'''
        for cr in Car.objects.all():
            sup = r.choice(Supplier.objects.all())
            car_price = Decimal(str(r.uniform(1_000, 100_000))).quantize(Decimal('1.00'))

            SupplierGarage.objects.create(
                car=cr,
                supplier=sup,
                price=car_price,
            )

        '''Supplier promotion.'''
        all_supplier = Supplier.objects.all()

        for sup in all_supplier:
            if len(SupplierGarage.objects.filter(supplier=sup)):
                # Get all cars for one supplier
                each_sup_cars = r.sample(
                    list(SupplierGarage.objects.filter(supplier=sup)),
                    r.randint(10, len(SupplierGarage.objects.filter(supplier=sup)))
                )

                for each_car in each_sup_cars:
                    SupplierPromo.objects.create(
                        supplier=sup,
                        car=each_car,
                        discount=r.randint(1, 50)
                    )

        print("===< Database filling completed successfully >===", end='\n\n')
