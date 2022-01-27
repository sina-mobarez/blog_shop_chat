from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail

from django.db.models.aggregates import Count

from django.forms.models import modelformset_factory
from django.http.response import BadHeaderError, HttpResponse, JsonResponse


from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .permissions import IsSellerMixin

from .forms import *
from .models import *




@method_decorator(login_required, name='dispatch')
class Dashboard(IsSellerMixin, ListView):
    template_name = "dashboard-shop.html"
    context_object_name = 'shop'
    paginate_by = 3
    
    
    def get_queryset(self):
        return Shop.confirmed.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
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
class CategoryDetail(IsSellerMixin, DetailView):

    model = Category
    context_object_name = 'categories'
    template_name = "filter_by_category.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context





@method_decorator(login_required, name='dispatch')
class TypeDetail(IsSellerMixin, DetailView):

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
class DeleteCategory(IsSellerMixin, DeleteView):
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('add-type-category')





@method_decorator(login_required, name='dispatch')
class DeleteType(IsSellerMixin, DeleteView):
    model = Type
    template_name = 'delete_type.html'
    success_url = reverse_lazy('add-type-category')






@method_decorator(login_required, name='dispatch')
class EditCategory(IsSellerMixin, UpdateView):
    model = Category
    fields = ['name',]
    template_name = 'edit_category.html'
    success_url = reverse_lazy('add-type-category')







@method_decorator(login_required, name='dispatch')
class EditType(IsSellerMixin, UpdateView):
    model = Type
    fields = ['name',]
    template_name = 'edit_type.html'
    success_url = reverse_lazy('add-type-category')







@method_decorator(login_required, name='dispatch')
class ShopDetail(IsSellerMixin, DetailView):
    model = Shop
    context_object_name = 'shop'
    template_name = "shop_detail.html"


    def get_context_data(self, **kwargs):
        print(self.object)
        context = super(ShopDetail, self).get_context_data(**kwargs)
        context['product_count'] = self.object.product_set.all().count()
        context['product'] = Product.objects.filter(shop=self.object)
        context['order'] = Cart.objects.filter(shop=self.object).order_by('-created_at')
        context['order_count'] = Cart.objects.filter(shop=self.object).count()
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        context['word'] = 'لیست سبد خرید'
        return context


    def post(self, request, *args, **kwargs):
        status = request.POST['status']
        if status == 'PID':
            word = 'پرداخت شده'
        elif status == 'CFD':
            word = 'تاییده شده'
        elif status == 'CNL':
            word = 'کنسل شده'
        else:
            word = 'در حال پردازش'
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['product_count'] = self.object.product_set.all().count()
        context['product'] = Product.objects.filter(shop=self.object)
        context['order'] = Cart.objects.filter(shop=self.object).filter(status_payment=status).order_by('-created_at')
        context['order_count'] = Cart.objects.filter(shop=self.object).filter(status_payment=status).count()
        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        context['word'] = word
        return self.render_to_response(context)


  
  
  




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
class CreateShop(IsSellerMixin, CreateView):
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
class DeleteShop(IsSellerMixin, UpdateView):
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
class UpdateShop(IsSellerMixin, UpdateView):
    model = Shop
    fields = ['name', 'type', 'description']
    template_name = 'update_shop.html'
    success_url = reverse_lazy('dashboard-shop')



    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.status = 'PEN'
        self.object.save()
        return super().form_valid(form)





@method_decorator(login_required, name='dispatch')
class AddTypeCategory(IsSellerMixin, View):
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





@login_required
def add_product(request, slug):
 
    ImageFormSet = modelformset_factory(Picture,form=PictureForm, extra=4)
    shop = get_object_or_404(Shop, slug=slug)
    
    
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
 
                if form:
                    image = form['image']
                    photo = Picture(product=product_form, image=image)
                    photo.save()
  
            messages.success(request,"Yeeew, check it out on the home page!")
            return redirect(f'http://127.0.0.1:8000/shop/dashboard/{slug}')
        else:
            print(productForm.errors, formset.errors)
    else:
        postForm = ProductForm()
        formset = ImageFormSet(queryset=Picture.objects.none())
    return render(request, 'add_product.html',
                  {'postForm': postForm, 'formset': formset})






@method_decorator(login_required, name='dispatch')
class ProductDetail(IsSellerMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"


    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['shop'] = Shop.objects.filter(owner=self.request.user).filter(product=self.object)
    
        context['image'] = Picture.objects.filter(product=self.object)

        context['types'] = Type.objects.filter(shop__owner=self.request.user).distinct().annotate(count_shop=Count('shop'))
        context['category'] = Category.objects.filter(product__owner=self.request.user).distinct().annotate(count_product=Count('product'))
        return context





@method_decorator(login_required, name='dispatch')
class Editproduct(IsSellerMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'quantity']
    template_name = 'update_product.html'
    success_url = reverse_lazy('dashboard-shop')




@method_decorator(login_required, name='dispatch')
class DeleteProdcut(IsSellerMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('dashboard-shop')





@method_decorator(login_required, name='dispatch')
class CartDetail(IsSellerMixin, DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name = "cart-detail.html"


    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['items'] = CartItem.objects.filter(cart=self.object)
        status = self.object.status_payment
        if status == 'PID':
            word = 'پرداخت شده'
            color = 'success'
            set = 'Paid'
        elif status == 'CFD':
            word = 'تاییده شده'
            color = 'primary'
            set = 'Confirmed'
        elif status == 'CNL':
            word = 'کنسل شده'
            color = 'danger'
            set = 'Canceled'
        else:
            word = 'در حال پردازش'
            color = 'warning'
            set = 'Pending'

        context['word'] = word
        context['color'] = color
        context['status'] = set
        context['value'] = status

        return context


    def post(self, request, *args, **kwargs):
        item_id = request.POST['cart_id']
        item = CartItem.objects.get(pk=item_id)
        item.delete()
        cart = self.get_object()
        cart.save()
        messages.success(request,"آیتم مورد نظر از سبد خرید کاربر حذف شد")
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)





@method_decorator(login_required, name='dispatch')
class SearchByDate(IsSellerMixin, View):
    def post(self, request, *args, **kwargs):
        shop = kwargs['slug']
        start = request.POST.get('startdate', None)
        end = request.POST.get('enddate', None)
        carts = Cart.objects.filter(shop__slug=shop).filter(created_at__date__range=(start, end))
        return render(request, 'search_by_date.html', {'cart': carts})

    def get(self, request, *args, **kwargs):
        shop = kwargs['slug']
        carts = Cart.objects.filter(shop__slug=shop)
        return render(request, 'search_by_date.html', {'cart': carts})




@login_required
def change_status(request):
    status = request.GET.get('status', None)
    id = request.GET.get('cartid', None)
    cartitem = Cart.objects.get(pk=id)
    cartitem.status_payment = status
    cartitem.save()
    data = {
        'is_taken': 'status is change'
    }
    subject = f'تغییر در وضعیت سبد خرید { cartitem.shop }'
    message = f'سبد خرید شماره ی  { cartitem.order_number} توسط فروشگاه دار به حالت {status} تغییر یافت . با تچکر '
    sender = f'فروشگاه {cartitem.shop}'
    recipients = [cartitem.owner.email]
    try:
        send_mail(subject, message, sender, recipients, fail_silently=True)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    return JsonResponse(data)





class LandingPage(TemplateView):

    template_name = "landing.html"




class NotpermissionOr404(TemplateView):

    template_name = "404.html"




class ReportSale(IsSellerMixin, ListView):
    template_name = "report.html"
    context_object_name = 'report'
    
    
    def get_queryset(self):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        user_list = []
        user_list2 = []
        
        for item in shop.cart_set.all().filter(status_payment='PID').distinct():
            user_list.append(item)


        for item in shop.cart_set.all().filter(status_payment='PID').distinct():
            user_list2.append(item.customer)

        count_list = []
        for user in user_list2:
            count = Cart.objects.filter(customer=user, shop=shop, status_payment='PID').count()
            count_list.append(count)

        list_data = zip(user_list, count_list)
    
        return list_data



    def get_context_data(self, **kwargs):
        context = super(ReportSale, self).get_context_data(**kwargs)
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        cart = []
        for item in shop.cart_set.all():
            if item.status_payment == 'PID':
                cart.append(item)
        January = []
        February = []
        March = []
        April = []
        May = []
        June = []
        July = []
        August = []
        September = []
        October = []
        November = []
        December = []

        for item in cart:
            if item.paid_date.month == 1:
                January.append(item)
            elif item.paid_date.month == 2:
                February.append(item)
            elif item.paid_date.month == 3:
                March.append(item)
            elif item.paid_date.month == 4:
                April.append(item)
            elif item.paid_date.month == 5:
                May.append(item)
            elif item.paid_date.month == 6:
                June.append(item)
            elif item.paid_date.month == 7:
                July.append(item)
            elif item.paid_date.month == 8:
                August.append(item)
            elif item.paid_date.month == 9:
                September.append(item)
            elif item.paid_date.month == 10:
                October.append(item)
            elif item.paid_date.month == 11:
                November.append(item)
            elif item.paid_date.month == 12:
                December.append(item)
        data = [len(January), len(February), len(March), len(April), len(May), len(June), len(July), len(August),
        len(September), len(October), len(November), len(December)]

        context['data'] = data
        return context

