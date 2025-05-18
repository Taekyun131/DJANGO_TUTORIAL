from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):   # BasePermission을 상속해서 커스텀 권한 클래스를 생성
    # GET: 누구나, PUT/PATCH: 해당유저만
    def has_object_permission(self, request, view, obj):    #  객체 수준 권한 검사
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS는 읽기 전용 메서드 목록
            return True
        return obj.user==request.user   # 해당 객체(obj)의 user가 현재 요청을 보낸 사용자(request.user)와 같을 때만 허용(본인만 수정 가능)