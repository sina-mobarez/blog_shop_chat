from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        class Meta(UserCreationForm.Meta):
             model = get_user_model()
             fields = ('email', 'username', 'phone', 'password1', 'password2')




class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username/ PhoneNumbr')