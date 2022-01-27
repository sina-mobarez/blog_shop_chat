from .views import VerifyPhoneNumber, GetCodeForVerify
from django.urls import path




urlpatterns = [
    
    path('verify-phone-number/', VerifyPhoneNumber.as_view(), name='verify-phone-number'),
    path('get-code-for-verify/', GetCodeForVerify.as_view(), name='get-code-for-verify'),

]
