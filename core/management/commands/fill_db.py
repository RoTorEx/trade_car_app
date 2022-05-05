from django.core.management.base import BaseCommand
from django_countries import data as countries_data

import datetime
import random as r
from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal

from user.models import UserProfile
from car.models import Car, engine, color, trans
from buyer.models import Buyer
from supplier.models import Supplier, SupplierGarage
from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory


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


def usr(usr_role, name, verify=False):
    '''Role distributing method.'''
    UserProfile.objects.create(
        username=name,
        email=Faker().email(),
        password='9ol8ik7uj',
        role=usr_role,
        verifyed_email=verify,
    )


class Command(BaseCommand):
    help = '''Expanding the functionality of the basic app commands.'''

    def handle(self, *args, **options):

        # Create superusers
        if not UserProfile.objects.filter(username__in=('root', 'admin')):
            UserProfile.objects.create_superuser('root', 'root@example.com', '1234')
            UserProfile.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print('\nSuperusers created success!\n')

        # Clea databases
        UserProfile.objects.filter(is_superuser=False).delete()
        Car.objects.all().delete()
        Buyer.objects.all().delete()
        Supplier.objects.all().delete()
        Dealership.objects.all().delete()
        DealershipGarage.objects.all().delete()
        DealershipBuyHistory.objects.all().delete()

        fake = Faker()
        fake.add_provider(Provider)  # Register custom Faker class

        # Variables
        count_cars = 128
        count_buyers = 24
        count_suppliers = 8
        count_dealership = 12

        # Car
        for _ in range(count_cars):
            car = r.choice(list(brand_model.keys()))

            Car.objects.create(
                car_brand=car,
                car_model=r.choice(brand_model[car]),
                engine_type=r.choice(engine)[0],
                transmission=r.choice(trans)[0],
                color=r.choice(color)[0],
                description=fake.text(),
            )

        # Staff Users
        for i in range(12):
            name = str(i) + 'app_user'
            verify = True
            usr('staff', name, verify)

        # Buyer
        for _ in range(count_buyers):
            name = Faker().user_name()
            usr('buyer', name)

            Buyer.objects.create(
                user=UserProfile.objects.latest('id'),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                balance=Decimal(str(r.uniform(100, 100_000))).quantize(Decimal('1.00')),
            )

        # Supplier
        for _ in range(count_suppliers):
            name = Faker().user_name()
            usr('supplier', name)

            Supplier.objects.create(
                user=UserProfile.objects.latest('id'),
                name=fake.company(),
                year_of_foundation=datetime.date(r.randint(1900, 2022), r.randint(1, 12), r.randint(1, 28)),
            )

        # Dealership
        for _ in range(count_dealership):
            name = Faker().user_name()
            usr('dealership', name)

            brand = list(set([r.choice(list(brand_model.keys())) for _ in range(5)]))
            model = []

            for i in brand:
                model += brand_model[i]

            eng = list(set([r.choice(engine)[0] for _ in range(2)]))
            transmission = list(set([r.choice(trans)[0] for _ in range(3)]))
            clr = list(set([r.choice(color)[0] for _ in range(6)]))

            Dealership.objects.create(
                user=UserProfile.objects.latest('id'),
                name=fake.dealer(),
                location=r.choice(list(countries_data.COUNTRIES.keys())),
                balance=Decimal(str(r.uniform(100_000, 100_000_000))).quantize(Decimal('1.00')),
                car_characters={
                    'car_brand': brand,
                    'car_model': model,
                    'engine_type': eng,
                    'transmission': transmission,
                    'color': clr,
                }
            )

        # Supplier cars
        for cr in Car.objects.all():
            sup = r.choice(Supplier.objects.all())
            car_price = Decimal(str(r.uniform(1_000, 500_000))).quantize(Decimal('1.00'))

            SupplierGarage.objects.create(
                car=cr,
                supplier=sup,
                price=car_price,
            )
