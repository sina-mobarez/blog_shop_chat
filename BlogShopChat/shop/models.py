from io import BytesIO
from os import name
from random import choice
import random
from PIL import Image
from django.template.defaultfilters import slugify


from django.core.files import File
from django.db import models

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + str(random.randint(0, 12000))
    return unique_slug


class MultiImage(models.Model):
    def get_default(self):
        return self.images.filter(default=True).first()

    def get_thumbnail_default(self):
        return self.images.filter(default=True).first().get_thumbnail()




class Image(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(MultiImage, on_delete=models.CASCADE)
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
    STATUS= [
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
    ]
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    type = models.CharField(max_length=150)
    status = models.Choices(max_length=3, choices=STATUS, default=PENDING)
    date_created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(MultiImage):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    quantity = models.DecimalField(max_digits=12) 
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    

    

    



