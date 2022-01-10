from django.shortcuts import render

# Create your views here.


from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer

# Create your views here.

class UserProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]