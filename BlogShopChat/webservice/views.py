from django.core.validators import validate_email
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse
from rest_framework import generics, mixins, viewsets, status
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.


from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Profile
from shop.models import Cart, CartItem, Product, Shop, Type
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import CartItemSerializer, CartSerializer, ConfirmedShop, TypeSerializer, UserProfileSerializer, ProductSerializer
from .filters import ShopListFilter, ProductListFilter

# Create your views here.

class UserProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)




# class userProfileViewSet(viewsets.ViewSet):
#     queryset = Profile.objects.all()
#     permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
#     print('innnjaaaaa')



#     def retrieve(self, request, user=None):
#         print('oooonjaaaa')
#         item = get_object_or_404(self.queryset, user=request.user)
#         serializer = UserProfileSerializer(item)
#         return Response(serializer.data)

class UserProfileRetrieveUpdateDelete(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Profile.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(request)
        file = request.data['file']
        instance.image = file
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



    def get_object(self, request):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.




        obj = get_object_or_404(queryset, user=request.user)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj



class ConfirmedShopList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Shop.confirmed.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = ShopListFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConfirmedShop



class TypeList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Type.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TypeSerializer



class ProductList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.filter(quantity__gt=1)
    filterset_class = ProductListFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer



class AddItemToCart(mixins.CreateModelMixin, generics.GenericAPIView):
 
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CartItemSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = request.data.product
        shop = product.shop
        print('shop----', shop) 
        have_pending_cart = Cart.objects.filter(customer=request.user, status_payment='PEN', shop=shop).count()
        if have_pending_cart > 1:
            cart = Cart.objects.filter(customer=request.user, status_payment='PEN').first()
        else:
            cart = Cart.objects.create(customer=request.user, shop=shop)
        item = self.perform_create(serializer)
        resp_serializer = CartSerializer(cart)
        headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED, headers=headers)