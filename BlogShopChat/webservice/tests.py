
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls.base import reverse
from model_mommy import mommy
from accounts.models import CustomUser
from shop.models import Cart, CartItem, Category, Product, Shop, Type


class UserProfileTestCase(APITestCase):
    
    
    def setUp(self):
        
        self.profile_list_url = reverse('all-profiles')
        self.profile_me_url = reverse('profile')
        self.shop_confirmed_url = reverse('confirmed-shop')
        self.type_list_url = reverse('type')
        self.product_list_url = reverse('product')
        self.add_item_to_cart_url = reverse('add-item-to-cart')
        self.cart_open_list_url = reverse('cart-open')
        self.cart_close_list_url = reverse('cart-close')

   
        self.owner = mommy.make(CustomUser,username='sina', password='i-keep-jumping', phone='9907841256', is_verified=True)


    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)


    def test_userprofile_list_authenticated(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_userprofile_list_without_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


    def test_user_can_see_self_profile(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.profile_me_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_user_can_see_self_profile_without_authenticated(self):
        res = self.client.get(self.profile_me_url)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')


    def test_shop_confirmed_list_work(self):
        Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.shop_confirmed_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], 'testShop')


    def test_shop_confirmed_list_when_doesnt_confirmed_shop(self):
        Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), owner=self.owner)
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.shop_confirmed_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)
        
        
    def test_shop_confirmed_list_whithout_authenticated(self):
        Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), owner=self.owner)
        res = self.client.get(self.shop_confirmed_url)
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')       


    def test_type_list_work(self):
        Type.objects.create(name='TestType')
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.type_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], 'TestType')
        
        
    def test_type_list_work_when_doesnt_exist_any_type(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.type_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)        


    def test_type_list_work_without_authenticated(self):
        res = self.client.get(self.type_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')

        
    def test_product_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.product_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
    def test_product_list_without_authenticated(self):
        res = self.client.get(self.product_list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)        

        
    def test_add_item_to_cart_work(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.add_item_to_cart_url, {'product':product.id, 'quantity':1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        
    def test_add_item_to_cart_work_without_authenticated(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        res = self.client.post(self.add_item_to_cart_url, {'product':product.id, 'quantity':1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)    
        
        
    def test_add_item_to_cart_when_wrong_data_give_them(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.add_item_to_cart_url, {'product':12, 'quantity':1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(res.data['product'], 'Incorrect type. Expected pk value, received str.')    


    def test_add_item_to_cart_when_wrong_i_want_buy_more_than_stack(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.add_item_to_cart_url, {'product':product.id, 'quantity':21}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['message'], 'you can not buy more than stock')   
        
        
        
    def test_cart_open_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.cart_open_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
    def test_cart_open_list_without_authenticated(self):
        res = self.client.get(self.cart_open_list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_cart_close_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.cart_close_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
    def test_cart_close_list_without_authenticated(self):
        res = self.client.get(self.cart_close_list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_cart_payment_work(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        cart = Cart.objects.create(shop=shop, customer=self.owner)
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(cart.status_payment, 'PND')
        res = self.client.put(reverse('cart-payment', kwargs={'pk':cart.id}))
        self.assertEqual(res.status_code, 200)
        
        
    def test_cart_payment_work_when_give_them_wrong_data(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        cart = Cart.objects.create(shop=shop, customer=self.owner)
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(cart.status_payment, 'PND')
        res = self.client.put(reverse('cart-payment', kwargs={'pk':114}))
        self.assertEqual(res.status_code, 404)
        
        
    
    def test_remove_product_from_cart_work(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        cart = Cart.objects.create(shop=shop, customer=self.owner)
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        self.client.force_authenticate(user=self.owner)
        res = self.client.delete(reverse('cart-romove-product', kwargs={'cart_id':cart.id, 'product_id':product.id}))
        self.assertEqual(res.status_code, 200)
        
        
    def test_remove_product_from_cart_work_when_give_them_wrong_data(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        cart = Cart.objects.create(shop=shop, customer=self.owner)
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        self.client.force_authenticate(user=self.owner)
        res = self.client.delete(reverse('cart-romove-product', kwargs={'cart_id':12, 'product_id':22}))
        self.assertEqual(res.status_code, 404)
             
