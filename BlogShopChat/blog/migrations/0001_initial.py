# Generated by Django 3.2.9 on 2021-12-31 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of category')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of tag start with #')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(blank=True)),
                ('bodytext', models.TextField(verbose_name='message')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='image')),
                ('post_date', models.DateTimeField(auto_now_add=True, verbose_name='post date')),
                ('modified', models.DateTimeField(blank=True, null=True, verbose_name='modified')),
                ('allow_comments', models.BooleanField(default=True, verbose_name='allow comments')),
                ('comment_count', models.IntegerField(blank=True, default=0, verbose_name='comment count')),
                ('status', models.CharField(choices=[('PUB', 'publish'), ('DRF', 'draft')], default='PUB', max_length=3, verbose_name='status of post')),
                ('category', models.ManyToManyField(to='blog.Category', verbose_name='category of this post')),
                ('likes', models.ManyToManyField(related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='likes on post')),
                ('posted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='posted by')),
                ('tag', models.ManyToManyField(to='blog.Tag', verbose_name='tags of this post')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-post_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('likes', models.ManyToManyField(related_name='blog_comments', to=settings.AUTH_USER_MODEL, verbose_name='likes on post')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='name of user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
