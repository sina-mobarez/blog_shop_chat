from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views.generic import ListView

from shop.admin import PictureAdmin
from .models import *
# Create your views here.

class Dashboard(ListView):
    template_name = "dashboard-shop.html"
    context_object_name = 'shop'
    paginate_by = 3
    
    
    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        print(Category.objects.filter(product__owner=self.request.user))
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if len(Shop.pending.filter(owner=self.request.user)) > 0:
            context['have_shop_pending'] = True
        else:
            context['have_shop_pending'] = False
        context['shop_pending'] = Shop.pending.filter(owner=self.request.user).first()
        context['types'] = Type.objects.annotate(count_shop=Count('shop')).filter(shop__owner=self.request.user).distinct()
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct()
        context['product'] = Product.objects.filter(owner=self.request.user)
        return context