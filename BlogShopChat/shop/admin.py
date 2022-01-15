
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import *


# Register your models here.
User = get_user_model()

class CustomerInline(admin.TabularInline):
    model = User

class ProductInline(admin.TabularInline):
    model = Product

class CartInline(admin.TabularInline):
    model = Cart

class CategoryInline(admin.TabularInline):
    model = Category


@admin.action(description='Mark selected shop as confirmed')
def make_confirmed(modeladmin, request, queryset):
    queryset.update(status='CON')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name','slug','type','status','date_created')
    list_filter = ('status','type','name')
    search_fields = ('name',)
    date_hierarchy = ('date_created')
    actions = [make_confirmed]

    fieldsets =(
        (None, {
            'fields': (('name', 'slug'), 'type', 'status', 'owner', 'description')
        }),
    )


    list_editable = ('status',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    list_filter = ('name',)
    search_fields = ('name',)



class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order_number', 'created_at', 'shop', 'status_payment', 'paid_amount', 'paid_date')
    list_filter = ('status_payment',)
    search_fields = ('order_number',)
    date_hierarchy = ('created_at')

    list_editable = ('status_payment',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart', 'quantity', 'price',)
    list_filter = ('price',)
    search_fields = ('cart',)


    list_editable = ('quantity',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category','name', 'slug', 'price', 'quantity', 'date_added', 'shop', 'show_image')
    list_filter = ('name', 'price', 'category')
    search_fields = ('name',)
    date_hierarchy = ('date_added')

    @admin.display(empty_value='-',description="image")
    def show_image(self, obj):
        if (obj.picture_set.all().first()):
            print('woooow',obj.picture_set.all().first().thumbnail.url)
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.picture_set.all().first().thumbnail.url,
                
            )
        return '-'


    list_editable = ('quantity', 'price')

class PictureAdmin(admin.ModelAdmin):
    list_display = ('product','name', 'default','image_test')
    list_filter = ('default',)
    search_fields = ('name',)

    @admin.display(empty_value='-',description="image")
    def image_test(self, obj):
        if (obj.thumbnail):
        
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.thumbnail.url,
                
            )
        return '-'

    fieldsets = (
        (None, {
            'fields': (('name', 'default'), 'image', 'product',)
        }),
    

        ('little more', {
            'classes': ('collapse',),
            'fields': ('thumbnail',),
        }),
    )



admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Type)



