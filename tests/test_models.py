from core.enums import UserRoles

import pytest
import random as r


pytestmark = pytest.mark.django_db


def test_user_model(users):
    user = r.choice(users)
    assert user._meta.get_field('username').max_length == 150
    assert user._meta.get_field('username').unique is True
    assert user._meta.get_field('role').choices == UserRoles.choices()
    assert user._meta.get_field('verifyed_email').default is False


def test_buyer_model(buyers):
    buyer = r.choice(buyers)
    assert buyer._meta.get_field('first_name').max_length == 255
    assert buyer._meta.get_field('last_name').max_length == 255
    assert buyer._meta.get_field('balance').max_digits == 10
    assert buyer._meta.get_field('balance').decimal_places == 2


def test_dealership_model(dealerships):
    dealership = r.choice(dealerships)
    assert dealership._meta.get_field('name').max_length == 255
    assert dealership._meta.get_field('balance').max_digits == 10
    assert dealership._meta.get_field('balance').decimal_places == 2


def test_supplier_model(suppliers):
    supplier = r.choice(suppliers)
    assert supplier._meta.get_field('name').max_length == 255
    assert supplier._meta.get_field('car_count').default == 0
