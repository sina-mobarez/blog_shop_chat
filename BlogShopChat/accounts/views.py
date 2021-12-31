from django.contrib.auth import authenticate, views as auth_views
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm, CustomUserCreationForm


class LoginView(auth_views.LoginView):


    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True





class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')