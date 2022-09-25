from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class TestUserAdmin(TestCase):
    """Test User Admin"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "adminuser@example.com",
            password = "password@1267"
        )
        
        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "password@1234"
        )

        self.client.force_login(self.user)
        self.client.force_login(self.admin_user)  

    def test_list_display(self):
        url = reverse('admin:core_user_changelist')
        res =  self.client.get(url)

        self.assertContains(res, self.user.email)
        # self.assertContains(res, self.user.name)

    def test_edit_user(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertTrue(res.status_code, 200)


    def test_add_user(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        
        self.assertContains(res, self.user.email)
        self.assertTrue(res.status_code, 201)