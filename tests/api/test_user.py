from rest_framework.test import force_authenticate, APITestCase, APIRequestFactory, URLPatternsTestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse, include, path

from user.models import UserProfile

import pytest
import random as r

pytestmark = pytest.mark.django_db


# def test_example(user):
#     factory = APIRequestFactory()
#     user = UserProfile.objects.get(username=user)
#     request = factory.get('api/user/me')
#     print(force_authenticate(request, user=user))


def test_create_user(client):
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


def test_user_me(users):
    client = APIClient()
    user = r.choice(users)

    client.force_authenticate(user=user)
    response = client.get("http://localhost/api/user/me/")
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert data['username'] == user.username
    assert data['id'] == user.id
