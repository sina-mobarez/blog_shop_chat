
from django.db.models.aggregates import Count
import django_filters


from shop.models import Product, Shop






class ShopListFilter(django_filters.FilterSet):
    type__name = django_filters.CharFilter(method='filter_type')
    product_count = django_filters.NumberFilter(method='filter_product_count')
    tag__name__contains = django_filters.CharFilter(method='filter_type_contains')

    
    class Meta:
        model = Shop
        fields = {
            'name': ['contains', 'icontains','exact'], 
        }

    def filter_type(self,queryset, key, value):
        queryset = queryset.filter(type__name=value)
        return queryset

    def filter_product_count(self,queryset, key, value):
        queryset = queryset.annotate(product_count=Count('product')).filter(product_count=value)
        return queryset


    def filter_type_contains(self,queryset, key, value):
        queryset = queryset.filter(type__name__contains=value)
        return queryset





class ProductListFilter(django_filters.FilterSet):
    shop__name = django_filters.CharFilter(method='filter_shop')
    category__name = django_filters.CharFilter(method='filter_category')
    owner__name = django_filters.CharFilter(method='filter_owner')
    shop__name__contains = django_filters.CharFilter(method='filter_shop_contains')
    available = django_filters.BooleanFilter(method='filter_available')
    
    class Meta:
        model = Product
        fields = {
            'name': ['contains', 'icontains','exact'],
            'price': ['gt', 'lt', 'exact'],
            'quantity': ['gt', 'lt', 'exact']
        }

    def filter_shop(self,queryset, key, value):
        queryset = queryset.filter(shop__name=value)
        return queryset

    def filter_shop_contains(self,queryset, key, value):
        queryset = queryset.filter(shop__name__contains=value)
        return queryset


    def filter_category(self,queryset, key, value):
        queryset = queryset.filter(category__name=value)
        return queryset


    def filter_owner(self,queryset, key, value):
        queryset = queryset.filter(owner__name=value)
        return queryset

    def filter_available(self, queryset, key, value):
        queryset = queryset.filter(available=value)