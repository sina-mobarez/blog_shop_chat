from django.views.generic.base import TemplateView
from .views import *
from django.urls import path
from django.urls import path

from .views import *

urlpatterns = [
    path('all_post/', PostList.as_view(), name="post_list"),
    path('all_post/<slug:slug>/', post_detail, name='post_detail'),
    path('all_post/<int:pk>', CategoryDetail.as_view(), name='post-category'),
    path('tag/<int:pk>', TagDetail.as_view(), name='post-tag'),
    path('add_post/', add_post, name='add_post'),
    path('contact/', contact_form, name='contact'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('all_post/<slug:slug>/edit/', edit_post, name='edit_post'),
    path('dashboard/new_post', add_post, name='new_post'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordChangeView.as_view(),{'template_name': 'registration/password_change_form.html'} , name='password_change'),
    path('search/', search, name='search'),
    path('like/<slug:slug>', LikeView, name='like_post'),
    path('post/<slug:slug>', change_status_post, name='change_status_post'),
    path('like_cm/<int:id>', Like_comment, name='like_comment'),
    path('add/', add_category_tag, name='add-cat-tag'),
    path('delete/<int:id>', delete_c, name='delete-c'),
    path('delete-t/<int:id>', delete_t, name='delete-t'),
    path('edit-t/<int:id>', edit_t, name='edit-t'),
    path('edit-c/<int:id>', edit_c, name='edit-c'),
    path('delete-post/<slug:slug>', delete_post, name='delete-post'),







]
