
import pdb
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy
from .models import CustomUser

class TestLoginRegisterVerifyGetCode(APITestCase):

    def setUp(self):

        self.register_url = reverse('api-register')
        self.login_url = reverse('api-login')
        self.verify_phone_number_url = reverse('verify-phone-number')
        self.get_code_for_verify_phone_number_url = reverse('get-code-for-verify')
        
        self.user_data_register = {
            'email': 'email@yahoo.vo',
            'username': 'emailvo',
            'phone': '9901232121',
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
        self.client.post(self.register_url, self.user_data_register, format="json")
        res = self.client.post(self.login_url,data=self.user_data_login, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], 'First verify your phone number')

        
    
    def test_user_can_get_code_for_verify_phone_number_correctly(self):
        user = mommy.make(CustomUser, email='sina@sina.com', password='qwe123123', phone='9124547878')
        res = self.client.post(self.get_code_for_verify_phone_number_url, data={'phone': user.phone}, format='json')
        self.assertEqual(res.status_code, 200)
        
    
    def test_user_can_verify_phone_number(self):
        self.client.post(self.register_url, self.user_data_register, format="json")
        res = self.client.post(self.verify_phone_number_url, data={'phone': '9901232121', 'otp_code': '125698'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'The provided code did not match or has expired')
        
        
        