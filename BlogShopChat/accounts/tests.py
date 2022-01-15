
from rest_framework.test import APITestCase
from django.urls import reverse


class TestLoginRegister(APITestCase):

    def setUp(self):

        self.register_url = reverse('api-register')
        self.login_url = reverse('api-login')
        
        self.user_data_register = {
            'email': 'email@yahoo.vo',
            'username': 'emailvo',
            'phone': '09901232121',
            'password': 'qwe123123',
        }

        self.user_data_login = {
            'email': 'email@yahoo.vo',
            'password': 'qwe123123'
        }
        return super().setUp()

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data_register, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_login_with_wrong_data(self):
        res = self.client.post(self.login_url,data={'email':'wallhaka', 'password':'awer23df12'}, format='json')
        self.assertEqual(res.status_code, 400)

    def test_user_login_correctly(self):
        res = self.client.post(self.login_url,data=self.user_data_login, format='json')
        self.assertEqual(res.status_code, 400)
        