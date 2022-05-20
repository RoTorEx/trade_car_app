from rest_framework import status

from car.models import Car

import pytest
import random as r

pytestmark = pytest.mark.django_db


@pytest.mark.car
def test_create_car(client):
    payload = dict(
        car_brand='Honda',
        car_model='Civic 6 Type R',
        engine_type='gas',
        transmission='mt',
        color='yellow',
        description="Pyshka gonka petarda!",
        is_active=True,
    )

    response = client.post("http://localhost/api/car/", payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert payload['car_brand'] == response.data['car_brand']
    assert payload['car_model'] == response.data['car_model']


@pytest.mark.car
def test_car_list(client, cars):
    response = client.get("http://localhost/api/car/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 10


@pytest.mark.car
def test_car_characters(client, cars):
    car = r.choice(cars)
    response = client.get(f"http://localhost/api/car/{car.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert car.car_brand == response.data['car_brand']
    assert car.car_model == response.data['car_model']
    assert car.engine_type == response.data['engine_type']
    assert car.transmission == response.data['transmission']
    assert car.color == response.data['color']
    assert car.description == response.data['description']


@pytest.mark.car
def test_car_put(client, cars):
    car = r.choice(cars)
    payload = dict(
        car_brand='Honda',
        car_model='Civic Type R',
        engine_type='gas',
        transmission='mt',
        color='red',
        description="Pyshka gonka petarda, WOW!",
        is_active=True,
    )

    response = client.put(f"http://localhost/api/car/{car.id}/", payload, content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == car.id
    assert response.data['car_brand'] == payload['car_brand']
    assert (response.data['description'] == payload['description']) != car.description


@pytest.mark.car
def test_car_delete(client, cars):
    car = r.choice(cars)
    response = client.delete(f"http://localhost/api/car/{car.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Car.objects.all().count() == 10 - 1
