from rest_framework import serializers
from accounts.models import Profile
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'


