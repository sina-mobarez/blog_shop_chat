from django.contrib import admin
from django.db import models as django_models
from .models import *

# Register your models here.





from . import models


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_count',)



admin.site.register(models.Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

