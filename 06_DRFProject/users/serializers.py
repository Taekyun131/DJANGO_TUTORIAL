from django.contrib.auth.models import User     #Django에서 정의한 User 모델
from django.contrib.auth.password_validation import validate_password       # Django의 기본 패스워드 검증도구
from .models import Profile


from rest_framework import serializers
from rest_framework.authtoken.models import Token   # Token 모델
from rest_framework.validators import UniqueValidator   # 이메일 중복방지를 위한 검증도구

from django.contrib.auth import authenticate    # Django의 기본 authenticate 함수, TokenAuth방식으로 유저 인증


# 회원가입 시리얼라이저 
# 제대로 입력됐는지 검사, User를 실제로 생성, 로그인에 쓸 수 있는 Token 생성
class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일에 대한 중복검증
    )
    password=serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],     # 비밀번호에 대한 검증
    )
    password2=serializers.CharField(write_only=True, required=True) # 비밀번호 확인을 위한 필드
    
    class Meta:
        model=User
        fields=('username', 'password', 'password2', 'email')
        
    # 추가적으로 비밀번호 일치 여부를 확인
    def validate(self, data):       # serializer.is_valid() 호출될 때 자동 실행
        if data['password']!=data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
    
    def create(self, validated_data):   # serializer.save()를 호출하면 내부적으로 create() 호출
        # CREATE 요청에 대해 create 메서드를 오버라이딩, 유저를 생성하고 토큰을 생성
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])   # set_password()로 암호화
        user.save()
        token=Token.objects.create(user=user)
        return user
    
    
# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user=authenticate(**data)
        if user:
            token=Token.objects.get(user=user)  # 토큰에서 유저 찾아 응답
            return token
        raise serializers.ValidationError(
            {"error": "Unable to login with provided credentials"}
        )
        

# 프로필 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):   # ModelSerializer: 해당 모델의 필드에 맞춰 자동으로 필드를 생성
    class Meta:
        model=Profile
        fields=("nickname", "position", "subjects", "image")    # 모델 필드들을 명시