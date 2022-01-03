from django.views.generic.base import TemplateView
from .views import *
from django.urls import path
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name="dashboard-shop"),
    path('dashboard/<slug:slug>', ShopDetail.as_view(), name="shop-detail")








]
