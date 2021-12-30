from django.contrib import admin
from django.db import models as django_models
from django.utils.html import format_html
from .models import *

# Register your models here.





from . import models


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_count',)
    list_display = ('title','slug', 'bodytext', 'image')
    list_filter = ('post_date',)
    search_fields = ('title',)


    @admin.display(empty_value='-',description="image")
    def image(self, obj):
        if (obj.pic):
        
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.pic.url,
                
            )
        return '-'


    fieldsets = (
        (None, {
            'fields': ('title', 'bodytext','pic',('category', 'tag'))
        }),
    

        ('little more', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('body','name', 'post','created')
    list_filter = ('post',)
    search_fields = ('name',)




admin.site.register(models.Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)

