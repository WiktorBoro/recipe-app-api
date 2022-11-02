from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe

RECIPE_URL = reverse('recipes:main')
DETAIL_RECIPE_URL = reverse('recipes:detail')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_recipe(user, **params):
    defaults = {
        'title': 'Default title',
        'time_minutes': 22,
        'price': Decimal("5.25"),
        'description': "Default description",
        'link': 'http://test.com/recipe.pdf'
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='pass123',
            name='Test',
        )
        self.client = APIClient()

    def test_get_list_recipe(self):
        date1 = models.Recipe.objects.create(
            {
                'user': self.user,
                'title': 'test Title 1',
                'time_minutes': 2,
                'price': 4,
                'description': 'Test description 1'
            }
        )
        date2 = models.Recipe.objects.create(
            {
                'user': self.user,
                'title': 'test Title 2',
                'time_minutes': 5,
                'price': 4.5,
                'description': 'Test description 2'
            }
        )

        response = self.client.get(RECIPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response[0]['user'], date1.user)
        self.assertEqual(response[0]['title'], date1.title)
        self.assertEqual(response[1]['user'], date2.user)
        self.assertEqual(response[1]['title'], date2.title)
        for res in response:
            self.assertNotIn('time_minutes', res)
            self.assertNotIn('price', res)
            self.assertNotIn('description', res)

    def test_get_detail_recipe(self):
        date = models.Recipe.objects.create(
            {
                'user': self.user,
                'title': 'test Title 1',
                'time_minutes': 2,
                'price': 4,
                'description': 'Test description 1'
            }
        )

        response = self.client.get(DETAIL_RECIPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['user'], date.user)
        self.assertEqual(response['title'], date.title)
        self.assertEqual(response['time_minutes'], date.time_minutes)
        self.assertEqual(response['price'], date.price)
        self.assertEqual(response['description'], date.description)
        self.assertTrue(response.date['link'])


class PrivateRecipeApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='pass123',
            name='Test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_recipe(self):
        payload = {
            'user': self.user,
            'title': 'test Title',
            'time_minutes': 5,
            'price': 4.5,
            'description': 'Test description'
        }
        response = self.client.post(RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.date['title'], payload['title'])
        self.assertEqual(response.date['price'], payload['price'])
        self.assertEqual(response.date['description'], payload['description'])
        self.assertEqual(self.user.name, payload['user'])
        self.assertEqual(response.date['time_minutes'], payload['time_minutes'])
        self.assertTrue(response.date['link'])

    def test_send_empty_payload_to_recipe(self):
        payload = {}

        response = self.client.post(RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_try_create_empty_recipe(self):
        payload = {
            'user': '',
            'title': '',
            'time_minutes': '',
            'price': '',
            'description': ''
        }

        response = self.client.post(RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recipe(self):
        payload = {
            'user': self.user,
            'title': 'test Title',
            'time_minutes': 5,
            'price': 4.5,
            'description': 'Test description'
        }
        response = self.client.post(RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.date['title'], payload['title'])
        self.assertEqual(response.date['price'], payload['price'])
        self.assertEqual(response.date['description'], payload['description'])
        self.assertEqual(self.user.name, payload['user'])
        self.assertEqual(response.date['time_minutes'], payload['time_minutes'])
        self.assertTrue(response.date['link'])

    def test_delete_recipe(self):
        date = models.Recipe.objects.create(
            {
                'user': self.user,
                'title': 'test Title 1',
                'time_minutes': 2,
                'price': 4,
                'description': 'Test description 1'
            }
        )

        payload = {'pk': 1}

        response = self.client.delete(DETAIL_RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        with self.assertRaises(models.Recipe.DoesNotExist):
            models.Recipe.get(id=date.pk)


