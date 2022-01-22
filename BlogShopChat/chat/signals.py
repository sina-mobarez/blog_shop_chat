from django.dispatch import receiver

from shop.models import Cart, Shop
import chat.models
from shop.models import Shop, Cart
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Shop)
def create_chatroom(sender, instance, created, **kwargs):
    if created:
        chat.models.Chat.objects.create(roomname=instance.name)
        print('=============chatroom================create')
        
@receiver(post_save, sender=Shop)       
def update_chatroom(sender, instance, created, **kwargs):
    if created == False:
        if instance.status == 'CON':
            chatroom = chat.models.Chat.objects.get(roomname=instance.name )
            chatroom.is_active = True
            chatroom.save()
            print('=================chatroom is active===============')
            
@receiver(post_save, sender=Cart)         
def add_member_to_chatroom(sender, instance, created, **kwargs):
    if created:
        chatroom = chat.models.Chat.objects.get(roomname=instance.shop.name)
        user = instance.customer
        chatroom.members.add(user)
        chatroom.save()
        print('=================members added===============')