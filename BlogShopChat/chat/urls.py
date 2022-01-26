from django.urls import path

from .views import index, room, search
from django.contrib.auth import views




urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    
]