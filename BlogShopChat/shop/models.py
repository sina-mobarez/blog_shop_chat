from io import BytesIO
from os import name
from random import choice
import random
from PIL import Image
from django.conf import settings
from django.template.defaultfilters import slugify


from django.core.files import File
from django.db import models


class EliminatedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'ELM')

class PendingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'PEN')

class ConfirmedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'CON')

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + str(random.randint(0, 12000))
    return unique_slug

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    def get_default(self):
        return self.image_set.filter(default=True).first()

    def get_thumbnail_default(self):
        return self.image_set.filter(default=True).first().get_thumbnail()
    
    def get_absolute_url(self):
        return f'/{self.category}/{self.slug}/'



class Image(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/thumbnail', blank=True, null=True)
    default = models.BooleanField(default=False)

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''


    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''


    def make_thumbnail(self, image, size=(200, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Shop(models.Model):
    PENDING= 'PEN'
    CONFIRMED= 'CON'
    ELIMINATED= 'ELM'
    STATUS= [
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
        (ELIMINATED, 'eliminated'),
    ]
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    type = models.CharField(max_length=150)
    status = models.CharField(max_length=3, choices=STATUS, default=PENDING)
    date_created = models.DateTimeField(auto_now_add=True)

    objects= models.Manager()
    eliminated= EliminatedManager()
    pending= PendingManager()
    confirmed = ConfirmedManager()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
        




class Cart(models.Model):
    Paid = 'PID'
    Confirmed = 'CFD'
    Canceled = 'CNL'
    Pending = 'PND'
    CHOICES = [(Paid, 'paid'),(Canceled, 'canceled'),(Pending, 'pending'), (Confirmed, 'confirmed')]
    status_payment = models.CharField(max_length=3,choices= CHOICES, default=Pending)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    paid_date = models.DateTimeField(null=True, verbose_name=("date of paid"), blank=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.customer}'

    def save(self, *args, **kwargs):
        if not self.paid_amount:
            final_price = 0
            items = self.cartitem_set.all()
            for item in items:
                price = item.price
                quantity = item.quantity
                final_price += price * quantity
            self.paid_amount = final_price
        super().save(*args, **kwargs)



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=3,blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product_set.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} {self.cart}'


    

    

    


