
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models.aggregates import Count

from django.forms.models import modelformset_factory
from django.http import request


from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import *


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




class CategoryDetail(DetailView):

    model = Category
    context_object_name = 'categories'
    template_name = "filter_by_category.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        print('query------',self.object.product_set.all() )
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context



class TypeDetail(DetailView):

    model = Type
    context_object_name = 'type'
    template_name = "filter_by_type.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(TypeDetail, self).get_context_data(**kwargs)
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context


@method_decorator(login_required, name='dispatch')
class DeleteCategory(DeleteView):
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('add-type-category')



@method_decorator(login_required, name='dispatch')
class DeleteType(DeleteView):
    model = Type
    template_name = 'delete_type.html'
    success_url = reverse_lazy('add-type-category')



@method_decorator(login_required, name='dispatch')
class EditCategory(UpdateView):
    model = Category
    fields = ['name',]
    template_name = 'edit_category.html'
    success_url = reverse_lazy('add-type-category')





@method_decorator(login_required, name='dispatch')
class EditType(UpdateView):
    model = Type
    fields = ['name',]
    template_name = 'edit_type.html'
    success_url = reverse_lazy('add-type-category')





@method_decorator(login_required, name='dispatch')
class ShopDetail(DetailView):
    model = Shop
    context_object_name = 'shop'
    template_name = "shop_detail.html"
    ImageFormSet = modelformset_factory(Picture,form=PictureForm, extra=4)


    def get_context_data(self, **kwargs):
        print(self.object)
        context = super(ShopDetail, self).get_context_data(**kwargs)
        context['product_count'] = self.object.product_set.all().count()
        context['product'] = Product.objects.filter(shop=self.object)
        context['order'] = Cart.objects.filter(shop=self.object).order_by('-created_at')
        context['order_count'] = Cart.objects.filter(shop=self.object).count()
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



# for pemenantly deleted shop

# @method_decorator(login_required, name='dispatch')
# class DeleteShop(DeleteView):
#     model = Shop
#     template_name = 'delete_shop.html'
#     success_url = reverse_lazy('dashboard-shop')


@method_decorator(login_required, name='dispatch')
class DeleteShop(UpdateView):
    model = Shop
    fields = ['name', 'type']
    template_name = 'delete_shop.html'
    success_url = reverse_lazy('dashboard-shop')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.status = 'ELM'
        self.object.save()
        return super().form_valid(form)




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


# @login_required(login_url='login')
# def add_category_type(request):
#     category_form = CategoryForm()
#     tag_form = TypeForm()
#     category = Category.objects.all() 
#     tag = Type.objects.all()
#     if request.method == "POST":
#         print(request.POST)
#         if request.POST['forcefield'] == 'c':    
#             category_form = CategoryForm(request.POST)
#             if category_form.is_valid():
#                 category_form.save()
#                 return redirect('add-type-category')
#         elif request.POST['forcefield'] == 't':
#             tag_form = TypeForm(request.POST)
#             if tag_form.is_valid():
#                 tag_form.save()
#                 return redirect('add-type-category')
#     else:
#         tag_form = TypeForm()
#         category_form = CategoryForm()
#     return render(request, 'add-type-category.html', {'tags': tag, 'category': category,'catform': category_form, 'tagform': tag_form})


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
                print('------------------------clinead',category_form.cleaned_data)
                category_form.save()  
                return redirect('add-type-category')
        elif request.POST['forcefield'] == 't':
            type_form = TypeForm(request.POST)
            if type_form.is_valid():
                type_form.save()
                return redirect('add-type-category')

        return render(request, self.template_name, {'tags': self.type, 'category': self.category,'catform': category_form, 'tagform': type_form})



@login_required
def add_product(request, slug):
 
    ImageFormSet = modelformset_factory(Picture,form=PictureForm, extra=4)
    shop = get_object_or_404(Shop, slug=slug)
    #'extra' means the number of photos that you can upload   ^
    
    if request.method == 'POST':
    
        productForm = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Picture.objects.none())
    
    
        if productForm.is_valid() and formset.is_valid():
            product_form = productForm.save(commit=False)
            product_form.owner = request.user
            product_form.shop = shop
            product_form.save()
    
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Picture(product=product_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,"Yeeew, check it out on the home page!")
            return redirect(f'http://127.0.0.1:8000/shop/dashboard/{slug}')
        else:
            print(productForm.errors, formset.errors)
    else:
        print(shop)
        postForm = ProductForm()
        formset = ImageFormSet(queryset=Picture.objects.none())
    return render(request, 'add_product.html',
                  {'postForm': postForm, 'formset': formset})


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"


    def get_context_data(self, **kwargs):
        print(Picture.objects.filter(product=self.object))
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['shop'] = Shop.objects.filter(owner=self.request.user).filter(product=self.object)
    
        context['image'] = Picture.objects.filter(product=self.object)

        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context


@method_decorator(login_required, name='dispatch')
class Editproduct(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'quantity']
    template_name = 'update_product.html'
    success_url = reverse_lazy('dashboard-shop')


@method_decorator(login_required, name='dispatch')
class DeleteProdcut(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('dashboard-shop')


class CartDetail(DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name = "cart-detail.html"


    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['items'] = CartItem.objects.filter(cart=self.object)
        return context