from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from user.models import UserProfile

import pytest

pytestmark = pytest.mark.django_db


class TestUser(APITestCase):

    '''Class to test users API'''

    def test_user_create(self):
        url = reverse('register')
        data = {
            'email': 'aleks_strel_8v@mail.ru',
            'username': 'neon',
            'password': '9ol8ik7uj',
            'role': 'staff',
        }
        response = self.client.post(url, data)

        assert 'password' not in response.data.keys()
        assert response.data['username'] == data['username']
        assert response.data['email'] == data['email']
        assert response.status_code == status.HTTP_201_CREATED
        assert UserProfile.objects.count() == 1
        assert UserProfile.objects.get().username == 'neon'
