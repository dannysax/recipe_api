from django.test.testcases import TestCase
from django.contrib.auth import get_user_model

class TestUserModels(TestCase):
    """Test user models"""
 
    def test_create_user_with_email(self):
        email = "example@gmail.com"
        password = "password@123"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):

        email_list = [
            ("Okon@GMAIL.COM", "Okon@gmail.com"),
            ("okon@gMaIl.com", "okon@gmail.com")
        ]
        
        for email, normal in email_list:
            user =  get_user_model().objects.create_user(email=email, password="password@1234")
            self.assertEqual(user.email, normal)

    def test_user_no_email_value_error(self):
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
            email="",
            password="password@223"
        )
        self.assertTrue(ValueError)

    def test_createsuperuser(self):
        email = "example@gmail.com"
        user = get_user_model().objects.create_superuser(
               email=email, 
               password="password@12345"
               )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_verified)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
