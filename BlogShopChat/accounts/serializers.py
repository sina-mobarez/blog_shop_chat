from accounts.models import CustomUser
from rest_framework import serializers
from .models import CustomUser


class VerifyPhoneNumberSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(required=True, max_length=6)
    
    class Meta:
        model = CustomUser
        fields = ['phone', 'otp_code']
        
        
        
        
class GetCodeVerifyPhoneNumberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['phone',]