from rest_framework import status
from rest_framework.test import APIClient

from user.models import UserProfile

import pytest
import random as r

pytestmark = pytest.mark.django_db


@pytest.mark.supplier
def test_supplier_list(suppliers, superuser):
    client = APIClient()
    supplier = r.choice(suppliers)

    response = client.get("http://localhost/api/supplier/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=supplier.user)
    response = client.get("http://localhost/api/supplier/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1

    admin = UserProfile.objects.filter(username='admin').get()
    client.force_authenticate(user=admin)
    response = client.get("http://localhost/api/supplier/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 3


@pytest.mark.supplier
def test_supplier_id(suppliers, superuser):
    client = APIClient()
    supplier = r.choice(suppliers)

    response = client.get(f"http://localhost/api/supplier/{supplier.id}/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=supplier.user)
    response = client.get(f"http://localhost/api/supplier/{supplier.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == supplier.id
    assert response.data['user']['username'] == str(supplier.user)

    response = client.post(f"http://localhost/api/supplier/{supplier.id}/")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
