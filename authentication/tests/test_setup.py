from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.user_data = {
            'username': 'Nergal',
            'email': 'nergal@gmail.com',
            'password': '123456',
            'confirm_password': '123456'
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()