
import email
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy
from .models import CustomUser

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
            'username': 'emailvo',
            'password': 'qwe123123'
        }
        return super().setUp()

    
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data_register, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], self.user_data_register['email'])

    
    def test_user_login_with_wrong_data(self):
        res = self.client.post(self.login_url,data={'username':'wallhaka', 'password':'awer23df12'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_user_login_correctly(self):
        user = mommy.make(CustomUser, email='ali@ali.com', password='qwe123123')
        self.client.force_authenticate(user=user)
        res = self.client.post(self.login_url,data={'username':user.username, 'password':user.password}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['data']['email'], 'ali@ali.com')
        