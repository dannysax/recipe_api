import email
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model



def add_user(**params):
    """helper function to create new user"""
    user = get_user_model().objects.create_user(**params)
    return user

create_user_url = reverse("user:create")
token_url = reverse("user:token")
me_url = reverse("user:me")

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


    def test_token_generated(self):
        user_details = {
            "email": "testapp@example.com",
            "password": "obilokanempire123"
        }

        add_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"]
            }

        res = self.client.post(token_url, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_empty_password(self):
        user_details = {
            "email":"another@example.com",
            "password":"authenticpass221"
        }

        add_user(**user_details)

        payload = {
            "email": user_details["password"],
            "password": " "
        }

        res = self.client.post(token_url, payload)
        
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(me_url)
        self.assertEqual(res.status_code, 403)
        
class PrivateApiViews(TestCase):
    def setUp(self):
        self.user = add_user(
            name = "Danny T",
            email = "testuser@gmail.com",
            password = "p@ssword123"
        )

        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_retrieve_me(self):
        res = self.client.get(me_url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, {
            "email": self.user.email,
            "name": "Danny T"
        })

    def test_retrieve_me_post_not_allowed(self):
        res = self.client.post(me_url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_me(self):
        payload = {'name': 'Updated name', 'password': 'newpassword123'}
        res = self.client.patch(me_url, payload)

        self.user.refresh_from_db() 
        self.assertEqual(self.user.name, payload["name"])
        # self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
