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










]
