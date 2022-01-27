from rest_framework import generics, mixins, status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Profile
from shop.models import Cart, CartItem, Product, Shop, Type

from .serializers import CartItemSerializer, CartSerializer, ConfirmedShop, TypeSerializer, UserProfileSerializer, ProductSerializer
from .filters import ShopListFilter, ProductListFilter
from rest_framework.parsers import FormParser, MultiPartParser



class UserProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)




class UserProfileRetrieveUpdateDelete(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_field = 'slug'
    parser_classes = (FormParser, MultiPartParser)

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
    permission_classes = (IsAuthenticated,)
    serializer_class = TypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)








class ProductList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.filter(quantity__gt=1)
    filterset_class = ProductListFilter
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer





class AddItemToCart(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Cart.objects.filter(status_payment='PND').all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Cart.objects.filter(status_payment='PND', customer=request.user).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CartItemSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        shop = product.shop

        have_pending_cart = len(Cart.objects.filter(customer=request.user, status_payment='PND', shop=shop))
 


        if serializer.validated_data['quantity'] > product.quantity :

            return Response(
            {
                'message': 'you can not buy more than stock',
            },
            status= status.HTTP_403_FORBIDDEN
        )
        
        if int(have_pending_cart) >= 1:
            cart = Cart.objects.filter(customer=request.user, status_payment='PND').first()
        else:
            cart = Cart.objects.create(customer=request.user, shop=shop)
        lst = []
        for item in cart.cartitem_set.all():
            lst.append(item.product)
        if product in lst:

            return Response(
            {
                'message': 'this product already exists in your cart',
                'offered': 'you can change quantity of this product'
            },
            status= status.HTTP_403_FORBIDDEN
        )
        serializer.validated_data['cart'] = cart
        item = self.perform_create(serializer)
        resp_serializer = CartSerializer(cart)
        headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED, headers=headers)







class ListCartOpen(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(status_payment='PND').all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Cart.objects.filter(status_payment='PND', customer=request.user).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





class ListCartPrevious(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(status_payment='PID').all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Cart.objects.filter(status_payment='PID', customer=request.user).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





class Paymentcart(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.all()
       

    def get_serializer_class(self):
        return CartSerializer

    def get(self, request, *args, **kwargs):
        if self.get_object().customer == request.user:
            return self.retrieve(request, *args, **kwargs)
        return Response(
            {
                'message': 'you can not see this cart, becaz not yours',
                
            },
            status= status.HTTP_403_FORBIDDEN

        )
        

    def put(self, request, *args, **kwargs):
        if self.get_object().customer == request.user:
            return self.update(request, *args, **kwargs)
        return Response(
            {
                'message': 'you can not paid this cart, becaz not yours',
                
            },
            status= status.HTTP_403_FORBIDDEN

        )
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.status_payment = 'PID'
        instance.save()
        lst = []
        lst_item = []
        for item in instance.cartitem_set.all():
            lst.append(item.product)
            lst_item.append(item.quantity)

        for index, product in enumerate(lst):
            product.quantity -= lst_item[index]
            product.save()
            if product.quantity <= 0:
                product.available = False

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {
                'message': 'payment is success, your cart already paid',
                
            },
            status= status.HTTP_200_OK

        )



    def delete(self, request, *args, **kwargs):
        if self.get_object().customer == request.user:
            return self.destroy(request, *args, **kwargs)
        return Response(
            {
                'message': 'you can not delete this cart, becaz not yours',
                
            },
            status= status.HTTP_403_FORBIDDEN
        )






class RemoveProductFromCart(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'cart_id'

    def get_queryset(self):
        return Cart.objects.all()
       

    def get_serializer_class(self):
        return CartSerializer

    def get(self, request, *args, **kwargs):
        if self.get_object().customer == request.user:
            return self.retrieve(request, *args, **kwargs)
        return Response(
            {
                'message': 'you can not see this cart, becaz not yours',
                
            },
            status= status.HTTP_403_FORBIDDEN

        )
        



    def delete(self, request, *args, **kwargs):
        if self.get_object().customer == request.user:
            return self.destroy(request, *args, **kwargs)
        return Response(
            {
                'message': 'you can not delete this cart, becaz not yours',
                
            },
            status= status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=kwargs['cart_id'])
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)
        if cart_item in cart.cartitem_set.all():
            cart_item.delete()
        cart_now = get_object_or_404(Cart, pk=kwargs['cart_id'])
        if len(cart_now.cartitem_set.all()) < 1:
            cart_now.delete()   
        return Response(
            {
                'message': 'product remove from your cart',
                
            },
            status= status.HTTP_200_OK
        )

