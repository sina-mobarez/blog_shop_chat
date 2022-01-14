from .views import *
from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'profile', userProfileViewSet)

urlpatterns = [
    #gets all user profiles and create a new profile
    path("profile",UserProfileListCreateView.as_view(),name="all-profiles"),
    # retrieves profile details of the currently logged in user
    # path("profile/me/",include(router.urls)),
    path("profile/me",UserProfileRetrieveUpdateDelete.as_view(), name='profile'),
    path('shop/confirmed', ConfirmedShopList.as_view(), name='confirmed-shop'),
    path('type', TypeList.as_view(), name='type'),
    path('product', ProductList.as_view(), name='product'),
    path('cart/product', AddItemToCart.as_view(), name='add-item-to-cart'),
    path('cart/open', ListCartOpen.as_view(), name='cart-open'),
    path('cart/close', ListCartPrevious.as_view(), name='cart-close'),
    path('cart/<int:pk>/payment', Paymentcart.as_view(), name='cart-payment'),
    path('cart/product/add', AddProductToCart.as_view(), name='cart-add-product'),
    path('cart/<int:cart_id>/remove/product/<int:product_id>', RemoveProductFromCart.as_view(), name='cart-romove-product'),




]