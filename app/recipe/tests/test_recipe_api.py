from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipes:recipes-list')


def detail_url(recipe_id):
    return reverse('recipes:recipes-detail', args=[recipe_id])


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
        self.client = APIClient()

    def test_no_authorization_recipe_request(self):
        request1 = self.client.get(RECIPE_URL)
        request2 = self.client.post(RECIPE_URL)
        self.assertEqual(request1.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request2.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@test.com',
            password='pass123',
        )
        self.client.force_authenticate(self.user)

    def test_get_list_recipe(self):
        create_recipe(self.user)
        create_recipe(self.user)

        all_recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(all_recipe, many=True)

        response = self.client.get(RECIPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_detail_recipe(self):
        date = create_recipe(self.user)

        response = self.client.get(detail_url(date.pk))
        serializer = RecipeSerializer(date)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_get_only_own_recipe(self):
        new_user = create_user(email='newuser@test.pl', password='newuser')
        create_recipe(self.user)
        create_recipe(new_user)

        response = self.client.get(RECIPE_URL)
        get_all_user_objects = Recipe.objects.filter(user=self.user)

        serializer = RecipeSerializer(get_all_user_objects, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_recipe(self):
        payload = {
            'title': 'Default title',
            'time_minutes': 22,
            'price': Decimal("5.25"),
        }

        response = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

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
            'description': '',
            'link': ''
        }

        response = self.client.post(RECIPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_recipe(self):
        original_link = 'https://example.com/recipe.pdf'
        date = create_recipe(user=self.user, link=original_link)
        payload = {
            'title': 'New title',
        }
        response = self.client.patch(detail_url(date.pk), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date.refresh_from_db()
        self.assertEqual(date.title, payload['title'])
        self.assertEqual(date.link, original_link)
        self.assertEqual(date.user, self.user)

    def test_full_update_recipe(self):
        date = create_recipe(user=self.user)
        payload = {
            'title': 'New title',
            'time_minutes': 10,
            'price': Decimal("4.25"),
            'description': "New description",
            'link': 'http://test.com/new-recipe.pdf'
        }
        response = self.client.put(detail_url(date.pk), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(date, k), v)
        self.assertEqual(date.user, self.user)

    def test_delete_recipe(self):
        date = create_recipe(user=self.user)

        response = self.client.delete(detail_url(date.pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=date.pk)

    def test_update_user_error(self):
        new_user = create_user(email='newuser@new.pl', password='test1234')
        recipe = create_recipe(self.user)

        payload = {'user': new_user.id}

        self.client.patch(detail_url(recipe.id), payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_other_users_recipe_error(self):
        new_user = create_user(email='newuser@new.pl', password='test1234')
        recipe = create_recipe(user=new_user)

        response = self.client.delete(detail_url(recipe.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
