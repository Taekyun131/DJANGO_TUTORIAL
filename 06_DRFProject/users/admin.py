from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.

# Profile 모델은 확장된 사용자 정보니까 관리자 화면에서도 함께 한 번에 볼 수 있도록 설정

# Profile을 User 아래에 붙이기 위한 클래스(User 페이지 안에 Profile 정보가 같이 뜨도록 하는 역할)
class ProfileInline(admin.StackedInline):   # StackedInline: 관리자 페이지에서 Profile을 '접힌 블럭' 형태로 보여주는 형식
    model=Profile
    can_delete=False
    verbose_name_plural="profile"

# 새로운 UserAdmin 정의(관리자는 User를 수정할 때 Profile 정보도 함께 수정 가능)
class UserAdmin(BaseUserAdmin):
    inlines=(ProfileInline, )

# 기존 UserAdmin 제거하고 커스터마이징한 UserAdmin으로 다시 등록
admin.site.unregister(User)
admin.site.register(User, UserAdmin)