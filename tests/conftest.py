from rest_framework.test import APIClient
from django_countries import data as countries_data

from user.models import UserProfile
from buyer.models import Buyer
from dealership.models import Dealership
from supplier.models import Supplier

import pytest
import random as r
import datetime

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def user():
    user = UserProfile.objects.create(
        username='test',
        password='9ol8ik7uj',
        email='test@example.com',
        role='unknown',
        verifyed_email=True,
    )

    return user


@pytest.fixture
def buyer(user):
    buyer = Buyer.objects.create(
        user=user,
        first_name='Alex',
        last_name='Strelkov',
        balance=122_333.88,
    )

    return buyer


@pytest.fixture
def dealership(user):
    dealership = Dealership.objects.create(
        user=user,
        name='MotorLand',
        location=r.choice(list(countries_data.COUNTRIES.keys())),
        balance=10_384_014.88,
    )

    return dealership


@pytest.fixture
def supplier(user):
    supplier = Supplier.objects.create(
        user=user,
        name='Lupa & Pupa Inc.',
        year_of_foundation=datetime.date(r.randint(1900, 2022), r.randint(1, 12), r.randint(1, 28)),
        car_count=125,
    )

    return supplier
