from rest_framework import status
from rest_framework.test import APIClient

from user.models import UserProfile

import pytest
import random as r

pytestmark = pytest.mark.django_db


@pytest.mark.buyer
def test_buyer_list(buyers, superuser):
    client = APIClient()
    buyer = r.choice(buyers)

    response = client.get("http://localhost/api/buyer/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=buyer.user)
    response = client.get("http://localhost/api/buyer/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1

    admin = UserProfile.objects.filter(username='admin').get()
    client.force_authenticate(user=admin)
    response = client.get("http://localhost/api/buyer/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 5


@pytest.mark.buyer
def test_buyer_id(buyers, superuser):
    client = APIClient()
    buyer = r.choice(buyers)

    response = client.get(f"http://localhost/api/buyer/{buyer.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=buyer.user)
    response = client.get(f"http://localhost/api/buyer/{buyer.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == buyer.id
    assert response.data['user']['username'] == str(buyer.user)

    response = client.post(f"http://localhost/api/buyer/{buyer.id}/")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.buyer
def test_create_buyer_offer(client, buyers):
    payload = dict(
        is_active=True,
        buyer=r.choice(buyers).id,
        max_price=r.randrange(1, 1234567),
        active_status="open"
    )

    response = client.post("http://localhost/api/buyer_offer/", payload)

    assert response.status_code == status.HTTP_201_CREATED
