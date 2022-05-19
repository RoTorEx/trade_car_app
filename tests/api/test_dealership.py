from rest_framework import status
from rest_framework.test import APIClient

from user.models import UserProfile

import pytest
import random as r

pytestmark = pytest.mark.django_db


@pytest.mark.dealership
def test_dealership_list(dealerships, superuser):
    client = APIClient()
    dealership = r.choice(dealerships)

    response = client.get("http://localhost/api/dealership/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=dealership.user)
    response = client.get("http://localhost/api/dealership/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1

    admin = UserProfile.objects.filter(username='admin').get()
    client.force_authenticate(user=admin)
    response = client.get("http://localhost/api/dealership/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 8


@pytest.mark.dealership
def test_dealership_id(dealerships, superuser):
    client = APIClient()
    dealership = r.choice(dealerships)

    response = client.get(f"http://localhost/api/dealership/{dealership.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=dealership.user)
    response = client.get(f"http://localhost/api/dealership/{dealership.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == dealership.id
    assert response.data['user']['username'] == str(dealership.user)

    response = client.post(f"http://localhost/api/dealership/{dealership.id}/")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
