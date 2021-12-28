
from django.contrib import admin
from django.db import models
from .models import *

# Register your models here.




admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Image)



