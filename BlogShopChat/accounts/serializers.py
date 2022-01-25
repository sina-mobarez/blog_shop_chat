from django.forms import fields
from accounts.models import CustomUser
from rest_framework import serializers
from .models import CustomUser


class VerifyPhoneNumber(serializers.ModelSerializer):
    otp_code = serializers.CharField(required=True, max_length=6)
    
    class Meta:
        model = CustomUser
        fields = ['phone', 'otp_code']
        
        
class GetCodeVerifyPhoneNumber(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['phone',]