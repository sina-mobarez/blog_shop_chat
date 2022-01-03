from os import terminal_size
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.api import success
from django.db.models.aggregates import Count
from django.forms import fields
from django.http import request
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import condition
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import *

from shop.admin import PictureAdmin
from .models import *
# Create your views here.


@method_decorator(login_required, name='dispatch')
class Dashboard(ListView):
    template_name = "dashboard-shop.html"
    context_object_name = 'shop'
    paginate_by = 3
    
    
    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        print(self.request.user.shop_set.filter(status='PEN').first())
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if len(Shop.pending.filter(owner=self.request.user)) > 0:
            context['have_shop_pending'] = True
        else:
            context['have_shop_pending'] = False
        context['shop_pending'] = Shop.pending.filter(owner=self.request.user)
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        context['product'] = Product.objects.filter(owner=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class ShopDetail(DeleteView):
    model = Shop
    context_object_name = 'shop'
    template_name = "shop_detail.html"

    def get_context_data(self, **kwargs):
        print(self.object)
        context = super(ShopDetail, self).get_context_data(**kwargs)
        context['product'] = Product.objects.filter(shop=self.object)
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context




def shop_no_pending_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, redirect_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: False if len(u.shop_set.filter(status='PEN')) > 0 else True,
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@method_decorator(shop_no_pending_required(redirect_url='dashboard-shop'), name='dispatch')
class CreateShop(CreateView):
    form_class = ShopForm
    template_name = 'create_shop.html'
    success_url = reverse_lazy('dashboard-shop')


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            messages.success(request,"فروشگاه ثبت شد و در  صف انتظار تایید قرار گرفت")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



@method_decorator(login_required, name='dispatch')
class DeleteShop(DeleteView):
    model = Shop
    template_name = 'delete_shop.html'
    success_url = reverse_lazy('dashboard-shop')



@method_decorator(login_required, name='dispatch')
class UpdateShop(UpdateView):
    model = Shop
    fields = ['name', 'type']
    template_name = 'update_shop.html'
    success_url = reverse_lazy('dashboard-shop')



    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.status = 'PEN'
        self.object.save()
        return super().form_valid(form)



class AddTypeCategory(View):
    category_form = CategoryForm()
    type_form = TypeForm()
    category = Category.objects.all() 
    type = Type.objects.all()
    template_name = 'add-type-category.html'

    def get(self, request, *args, **kwargs):
        type_form = TypeForm()
        category_form = CategoryForm()
        category = Category.objects.all() 
        type = Type.objects.all()
        return render(request, self.template_name,{'tags': type, 'category': category,'catform': category_form, 'tagform': type_form})
    def post(self, request, *args, **kwargs):
        if request.POST['forcefield'] == 'c':    
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('add-type-category')
        elif request.POST['forcefield'] == 't':
            type_form = TypeForm(request.POST)
            if type_form.is_valid():
                type_form.save()
                return redirect('add-type-category')

        return render(request, self.template_name, {'tags': self.type, 'category': self.category,'catform': category_form, 'tagform': type_form})