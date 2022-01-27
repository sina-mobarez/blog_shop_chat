from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):

    class Meta:
            model = CustomUser
            fields = ('email', 'username', 'phone', 'password1', 'password2')




class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username/ PhoneNumbr')
    
    
    
    
class VerifyForm(forms.Form):
    forcefield = forms.CharField(required=False, widget=forms.HiddenInput())
    otp_code = forms.CharField(label='Code', max_length=6, required=True,
                        error_messages = {
                            'required' : 'the field is required',
                            'max_length' : 'max length exceeded'
                        }
    
                    )