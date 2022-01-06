from django.views.generic.base import TemplateView
from .views import *
from django.urls import path
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name="dashboard-shop"),
    path('dashboard/<slug:slug>', ShopDetail.as_view(), name="shop-detail"),
    path('create-shop/', CreateShop.as_view(), name="create-shop"),
    path('delete-shop/<slug:slug>', DeleteShop.as_view(), name='delete-shop'),
    path('update-shop/<slug:slug>', UpdateShop.as_view(), name='update-shop'),
    path('add-type-category', AddTypeCategory.as_view(), name='add-type-category'),
    path('add-product<slug:slug>/', add_product, name='add-product'),
    path('product/<slug:slug>', ProductDetail.as_view(), name='product-detail'),
    path('category-product/<slug:slug>', CategoryDetail.as_view(), name='category-product'),
    path('type-shop/<slug:slug>', TypeDetail.as_view(), name='type-shop'),
    path('delete-category/<slug:slug>', DeleteCategory.as_view(), name='delete-category'),
    path('edit-category/<slug:slug>', EditCategory.as_view(), name='edit-category'),
    path('delete-type/<slug:slug>', DeleteType.as_view(), name='delete-type'),
    path('edit-type/<slug:slug>', EditType.as_view(), name='edit-type'),
    path('edit-product/<slug:slug>', Editproduct.as_view(), name='edit-product'),
    path('delete-product/<slug:slug>', DeleteProdcut.as_view(), name='delete-product'),
    path('cart-detail/<int:pk>', CartDetail.as_view(), name='cart-detail'),
















]
