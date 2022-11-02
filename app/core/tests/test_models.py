"""
Tests for models.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models"""
    def test_create_user_with_email(self):
        """Test creating a user with an email is success"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_email = [
            ['test12e421@email.com', 'test12e421@email.com'],
            ['goop@Email.com', 'goop@email.com'],
            ['TEST@EMAIL.com', 'TEST@email.com'],
            ['Test22@EmaiL.com', 'Test22@email.com']
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_emial(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'password123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@test.pl',
            'Test123'
        )
        rec = models.Recipe.objects.create(
            user=user,
            title='Recipe title',
            time_minutes=5,
            price=Decimal('5.5'),
            description="Sample recipe description.",
        )

        self.assertEqual(str(rec), rec.title)

