from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):

    class Meta:
            model = CustomUser
            fields = ('email', 'username', 'phone', 'password1', 'password2')




class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username/ PhoneNumbr')