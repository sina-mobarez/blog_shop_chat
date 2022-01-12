import traceback
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.utils import model_meta
from accounts.models import Profile, CustomUser

from shop.models import Cart, CartItem, Product, Shop, Type, Category
 


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 2


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email']



class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model =Category
        fields = ['name']


class ConfirmedShop(serializers.ModelSerializer):
    owner = UserModelSerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    
    class Meta:
        model = Shop
        fields = ['name', 'slug', 'description', 'status', 'date_created', 'type', 'owner']



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = UserModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description','category', 'price', 'quantity', 'owner', 'shop', 'date_added']


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Cart
        fields = '__all__'