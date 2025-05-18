from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile
from .permission import CustomReadOnly
# Create your views here.
class RegisterView(generics.CreateAPIView):     # CreateAPIView(generics) 사용구현: 새 객체 생성(POST)
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    

class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request):    # POST 요청
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # 검증된 데이터는 validated_data에 저장
        token=serializer.validated_data # validate() 의 리턴값인 Token을 받아옴
        return Response({"token": token.key}, status=status.HTTP_200_OK)    # Token 객체의 key(토큰 값을) 응답으로 포함
 
# 사용자의 프로필 정보를 조회하고 수정할 수 있는 API 뷰 생성
class ProfileView(generics.RetrieveUpdateAPIView):      # GET 요청 → 특정 사용자의 프로필 정보를 조회
                                                        # PUT/PATCH 요청 → 특정 사용자의 프로필 정보를 수정
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[CustomReadOnly]     # 커스텀 권한 적용