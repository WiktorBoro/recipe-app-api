from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create-list')


def create_user(**params):
    return get_user_model().objets.create_user(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'TEST',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exist_error(self):
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'TEST',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email': 'test@test.com',
            'password': '123',
            'name': 'TEST',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # with self.assertRaises(ValueError):
        self.assertFalse(user_exists)
