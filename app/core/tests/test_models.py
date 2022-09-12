from django.test import SimpleTestCase
from django.contrib.auth import get_user_model

class TestUserModels(SimpleTestCase):
    """Test user models"""

    def test_create_user_with_email(self):
        email = "example@gmail.com"
        password = "password@123"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(email,email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        pass