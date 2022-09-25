import email
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model



def add_user(**params):
    """helper function to create new user"""
    user = get_user_model().objects.create(**params)
    return user

create_user_url = reverse("user:create")
class PublicUserApiTests(TestCase):
    """Test user model apis"""

    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        payload = {
            "email": "emai1@example.com",
            "password": "password124"
        }
        res = self.client.post(create_user_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_already_exists(self):
        """Test if user email already exists"""
        payload = {
            "email": "testmail@example.com",
            "password": "p@ssword2343"
        }
        add_user(email = payload["email"], password=payload["password"])
        res = self.client.post(create_user_url, data = payload
             )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_password_too_short_error(self):
        payload = {
            "email" : "solo@example.com",
            "password" : "123"
        }

        res = self.client.post(create_user_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
  

        

