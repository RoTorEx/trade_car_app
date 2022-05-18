from rest_framework.test import APIClient
from django_countries import data as countries_data

from user.models import UserProfile
from car.models import Car
from buyer.models import Buyer
from dealership.models import Dealership
from supplier.models import Supplier
from core.enums import Engine, Transmission, Color
from core.management.commands.fill_db import brand_model

from faker import Faker
import pytest
import random as r
import datetime

pytestmark = pytest.mark.django_db


def usr(name, usr_role):
    UserProfile.objects.create(
        username=name,
        email=Faker().email(),
        password='9ol8ik7uj',
        role=usr_role,
        verifyed_email=r.choice([True, False])
    )


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def superuser():
    superuser = UserProfile.objects.create_superuser('admin', 'admin@example.com', 'admin')

    return superuser


@pytest.fixture
def users():

    for postfix in ['One', 'Two', 'Three', 'Four', 'Five']:

        UserProfile.objects.create(
            username=f"User{postfix}",
            password='9ol8ik7uj',
            email=f"{postfix}_@example.com",
            role='unknown',
            verifyed_email=True,
        )

    users = UserProfile.objects.all()

    return users


@pytest.fixture
def cars():

    for _ in range(10):
        car = r.choice(list(brand_model.keys()))

        Car.objects.create(
            car_brand=car,
            car_model=r.choice(brand_model[car]),
            engine_type=r.choice(Engine.choices())[0],
            transmission=r.choice(Transmission.choices())[0],
            color=r.choice(Color.choices())[0],
            description=Faker().text(),
        )

    cars = Car.objects.all()

    return cars


@pytest.fixture
def buyers():

    for i in range(5):
        usr(f'UserBuyer{i}', 'buyer')

        Buyer.objects.create(
            user=UserProfile.objects.get(username=f'UserBuyer{i}'),
            first_name=Faker().first_name(),
            last_name=Faker().last_name(),
            balance=122_333.88,
        )

    buyers = Buyer.objects.all()

    return buyers


@pytest.fixture
def dealerships():

    for i in range(8):
        usr(f'UserDealership{i}', 'dealership')

        Dealership.objects.create(
            user=UserProfile.objects.get(username=f'UserDealership{i}'),
            name='MotorLand',
            location=r.choice(list(countries_data.COUNTRIES.keys())),
            balance=10_384_014.88,
        )

    dealerships = Dealership.objects.all()

    return dealerships


@pytest.fixture
def suppliers():

    for i in range(3):
        usr(f'UserSupplier{i}', 'supplier')

        Supplier.objects.create(
            user=UserProfile.objects.get(username=f'UserSupplier{i}'),
            name='Lupa & Pupa Inc.',
            year_of_foundation=datetime.date(r.randint(1900, 2022), r.randint(1, 12), r.randint(1, 28)),
            car_count=125,
        )

    suppliers = Supplier.objects.all()

    return suppliers
