import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related
from django.db.models.signals import post_save
from django.urls import reverse
from django.template.defaultfilters import slugify

from .signals import save_comment


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'PUB')

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'DRF')



class Category(models.Model):
    name = models.CharField("name of category", max_length=50)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("post-category", kwargs={"pk": self.pk})


class Tag(models.Model):
    name = models.CharField("name of tag start with #", max_length=50)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("post-category", kwargs={"pk": self.pk})


# define a function to add some digit to end of slug >>>> for uniqueness
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + str(random.randint(0, 12000))
    return unique_slug


class Post(models.Model):
    PUBLISHED= 'PUB'
    DRAFT= 'DRF'
    STATUS= [
        (PUBLISHED, 'publish'),
        (DRAFT, 'draft'),
    ]
    title = models.CharField(max_length=200, verbose_name=("title"))
    slug = models.SlugField(blank=True)
    bodytext = models.TextField(verbose_name=("message"))
    pic = models.ImageField("image", upload_to='uploads', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name='category of this post')
    tag = models.ManyToManyField(Tag, verbose_name=("tags of this post"), blank=True, null=True)
    likes = models.ManyToManyField(User, verbose_name=("likes on post"), related_name= 'blog_posts')
    post_date = models.DateTimeField(
        auto_now_add=True, verbose_name="post date")
    modified = models.DateTimeField(null=True, verbose_name=("modified"), blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                  verbose_name=("posted by"),
                                  on_delete=models.SET_NULL)

    allow_comments = models.BooleanField(
        default=True, verbose_name=("allow comments"))
    comment_count = models.IntegerField(
        blank=True, default=0, verbose_name=('comment count'))
    status= models.CharField('status of post', max_length=3, choices=STATUS, default=PUBLISHED)

    objects= models.Manager()
    published= PublishedManager()
    draft= DraftManager()

    class Meta:
        verbose_name = ('post')
        verbose_name_plural = ('posts')
        ordering = ['-post_date']

    def total_likes(self):
        return self.likes.count()

    # override the save method for store unique slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # a method that give us slug for linking detail of post instance
    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }

        return reverse('post_detail', kwargs=kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, verbose_name=("name of user"), on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, verbose_name=("likes on post"), related_name= 'blog_comments')

    class Meta:
        ordering = ('created',)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    # Hear a signal to save count of comment





post_save.connect(save_comment, sender=Comment)
