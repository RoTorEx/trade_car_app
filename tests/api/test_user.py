from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from user.models import UserProfile

import pytest
import random as r

pytestmark = pytest.mark.django_db


@pytest.mark.user
def test_register_user(client):
    url = reverse('register')
    data = {
        'email': 'aleks_strel_8v@mail.ru',
        'username': 'neon',
        'password': '9ol8ik7uj',
        'role': 'staff',
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == data['username']
    assert response.data['email'] == data['email']
    assert 'password' not in response.data.keys()
    assert UserProfile.objects.count() == 1
    assert UserProfile.objects.get().username == 'neon'


@pytest.mark.user
def test_login_user(client, superuser):
    url = reverse('login')
    data = {
        'username': 'admin',
        'password': 'admin',
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == data['username']
    assert 'access' in response.data['tokens']
    assert 'refresh' in response.data['tokens']
    assert 'password' not in response.data


@pytest.mark.user
def test_user_me(users):
    client = APIClient()
    user = r.choice(users)

    response = client.get("http://localhost/api/user/me/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)
    response = client.get("http://localhost/api/user/me/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username
    assert response.data['id'] == user.id

    client.force_authenticate(user=user)
    response = client.get("http://localhost/api/user/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 5
