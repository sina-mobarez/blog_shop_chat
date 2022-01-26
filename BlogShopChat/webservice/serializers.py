from rest_framework import serializers

from accounts.models import Profile, CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

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

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ['email', 'phone','username', 'password',]
        
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            phone=validated_data['phone'],
            email=validated_data['email'],
            username=validated_data['username']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user





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
        fields = ['id', 'name', 'slug', 'description','category', 'price', 'quantity', 'owner', 'shop', 'date_added']





class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']




class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'





class CartSerializer(serializers.ModelSerializer):
    customer = UserModelSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model =  Cart
        fields = ['id', 'status_payment', 'customer', 'products', 'order_number', 'shop', 'created_at', 'paid_amount', ]
        




class PaymentCartSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()





class AddProductToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'cart']
        
       
       
       
        
class UserModelLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        