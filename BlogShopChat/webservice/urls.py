from .views import *
from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'profile', userProfileViewSet)

urlpatterns = [
    #gets all user profiles and create a new profile
    path("all-profiles",UserProfileListCreateView.as_view(),name="all-profiles"),
    # retrieves profile details of the currently logged in user
    # path("profile/me/",include(router.urls)),
    path("profile/me/",UserProfileRetrieveUpdateDelete.as_view()),
    path('confirmed-shop/', ConfirmedShopList.as_view(), name='confirmed-shop'),
    path('type/', TypeList.as_view(), name='type'),
    path('product', ProductList.as_view(), name='product'),
]