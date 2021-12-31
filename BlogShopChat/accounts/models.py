from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _

from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


import random
import os
import requests

class UserManager(BaseUserManager):
   
    def create_user(self, username, email, phone, password, **extra_fields):
        """
        Create and save a User with the given email, phone number and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not phone:
            raise ValueError('The Phone must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, phone number and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, phone, password, **extra_fields)


class Country(models.Model):
    name = models.CharField(_("name of country"), max_length=50)


class City(models.Model):
    name = models.CharField(_("name of city"), max_length=50)
    country = models.ForeignKey(Country, verbose_name=_("country of city"), on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    phone_regex = RegexValidator( regex = r'^\+98\d{10}$', message ="Phone number must be entered in the format +989999999999. Up to 10 digits allowed.")
    phone = models.CharField('Phone number',validators =[phone_regex], max_length=14, unique=True,null=True)
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ['email', 'phone']
    is_seller = models.BooleanField(default=False)
    city = models.ForeignKey(City, verbose_name=_("where user is live"), on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length = 900, blank = True, null = True)


    objects = UserManager()  


    def __str__(self):
        return f'{self.phone} / {self.username}'     

