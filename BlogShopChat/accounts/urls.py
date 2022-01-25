from importlib.resources import path
from .views import *
from django.urls import path




urlpatterns = [
    path('verify-phone-number/', VerifyPhoneNumber.as_view(), name='verify'),
    path('get-code-for-verify/', GetCodeForVerify.as_view(), name='get-code-for-verify'),
]