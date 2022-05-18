from rest_framework import status
from rest_framework.test import APIClient

import pytest
import random as r

pytestmark = pytest.mark.django_db


def test_buyer_list(client, buyer):

    client = APIClient()

    client.force_authenticate(user=buyer.user)
    response = client.get("http://localhost/api/buyer/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
