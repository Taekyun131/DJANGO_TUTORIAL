# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Profile


# Create your views here.
# CreateAPIView(generics) 사용구현(회원가입 기능)
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    
    
# 로그인 구현
class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token=serializer.validated_data     # validate()의 리턴값인 Token을 받아옴
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
# 프로필 관련
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer