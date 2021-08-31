from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            'username': self.fake.email().split('@')[0],
            'email': self.fake.email(),
            'password': '123456',
            'confirm_password': '123456'
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()