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


    def test_user_can_see_self_profile(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.profile_me_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_shop_confirmed_list_work(self):
        Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.shop_confirmed_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], 'testShop')


    def test_type_list_work(self):
        Type.objects.create(name='TestType')
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.type_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], 'TestType')
        
        
    def test_product_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.product_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
    def test_add_item_to_cart_work(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.add_item_to_cart_url, {'product':product.id, 'quantity':1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        
    def test_cart_open_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.cart_open_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
    def test_cart_close_list_work(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.get(self.cart_close_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        
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
        
    
    def test_remove_product_from_cart_work(self):
        shop = Shop.objects.create(name='testShop', description='Shopinfo', type=Type.objects.create(name='testType'), status='CON', owner=self.owner)
        product = Product.objects.create(category= Category.objects.create(name='CatName'), name='TestProduct', description='Testapicase', price=45000, quantity=14, owner=
                                         mommy.make(CustomUser), shop=shop)
        cart = Cart.objects.create(shop=shop, customer=self.owner)
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        self.client.force_authenticate(user=self.owner)
        res = self.client.delete(reverse('cart-romove-product', kwargs={'cart_id':cart.id, 'product_id':product.id}))
        self.assertEqual(res.status_code, 200)
             
