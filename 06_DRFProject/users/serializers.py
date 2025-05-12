from django.contrib.auth.models import User     # Django에서 미리 정의해 놓은 User모델 사용
from django.contrib.auth.password_validation import validate_password   # Django의 기본 패스워드 검증 도구
from rest_framework import serializers
from rest_framework.authtoken.models import Token   # Token 모델
from rest_framework.validators import UniqueValidator   # 이메일 중복방지를 위한 검증도구
from django.contrib.auth import authenticate    # Django의 기본 authenticate함수, 
                                                # settings.py에서 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저 인증
from .models import Profile


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일에 대한 중복 검증
    )
    password=serializers.CharField(
        write_only=True,    # 서버로만 전송되고, 응답에는 포함하지 않음
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )
    password2=serializers.CharField(write_only=True, required=True) # 비밀번호 확인을 위한 필드
    
    class Meta:
        model=User
        fields=('username', 'password', 'password2', 'email')   # 시리얼라이즈에 필요한 필드 명시
    
    # 추가적으로 비밀번호 일치 여부를 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
    
    # CREATE요청에 대해 create 메서드를 오버라이딩, 유저를 생성하고 토큰을 생성
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])   # 비밀번호를 해싱해 저장
        user.save()
        token=Token.objects.create(user=user)
        return user
    

# 로그인 구현
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)
    # write_only 옵션을 통해 서버방향의 역직렬환는 가능, 클라이언트 방향의 직렬화는 불가능
    
    def validate(self, data):
        user=authenticate(**data)
        if user:
            token=Token.objects.get(user=user)  # 토큰에서 유저 찾아 응답
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("nickname", "position", "subjects", "image")