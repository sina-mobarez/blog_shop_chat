
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls.base import reverse
from model_mommy import mommy
from accounts.models import CustomUser
from shop.models import *
# Create your tests here.

class UserProfileTestCase(APITestCase):
    profile_list_url = reverse('all-profiles')
    def setUp(self):

        self.user = self.client.post('/auth/users/',data={'username':'mario', 'email':'email@gmail.com', 'phone':'09907841256','password':'i-keep-jumping'})
   
        response = self.client.post('/auth/jwt/create/',data={'username':'mario','password':'i-keep-jumping'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)


    def test_userprofile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_userprofile_detail_retrieve_without_authenticate(self):
        response = self.client.get(reverse('profile'))
        # print(response.data)
        self.assertEqual(response.status_code,200)


    def test_userprofile_profile_without_authenticate(self):
        profile_data = {'description':'I am a very famous game character','address':'nintendo world','is_creator':'true',}
        response = self.client.put(reverse('profile'),data=profile_data)
        print(response.data)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code,405)


class ViewsTest(APITestCase):

    def setUp(self):


        
        response = self.client.post('/auth/jwt/create/',data={'username':'admin','password':'admin'}, format='json')
        # self.token = response.data.refresh
        # self.api_authentication()


        self.confirmed_shop_list_url = reverse('confirmed-shop')
        self.type_url = reverse('type')
        self.product_list_url = reverse('product')
        self.create_cart_url = reverse('add-item-to-cart')
        self.cart_open_list_url = reverse('cart-open')
        self.cart_close_list_url = reverse('cart-close')
        self.add_item_to_product_url = reverse('cart-add-product')

        return super().setUp()


    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)




    def test_get_list_of_confirmed_shop(self):
        response = self.client.post('/auth/jwt/create/',data={'username':'admin','password':'admin'}, format='json')
        # user = CustomUser.objects.get(pk=1)
        # self.client.force_authenticate(user)
        res = self.client.get(self.confirmed_shop_list_url)

        import pdb
        pdb.set_trace()
        self.assertEqual(res.status_code, 403)

    # def test_get_type_of_shop(self):
    #     self.client.force_authenticate(self.user)
    #     res = self.client.get(self.type_url)

    #     self.assertEqual(res.status_code, 200)

    # def test_get_product_list(self):
    #     self.client.force_authenticate(self.user)
    #     res = self.client.put(self.product_list_url, data={'product': self.product}, format='json')

    #     import pdb
    #     pdb.set_trace()
    #     self.assertEqual(res.status_code, 200)