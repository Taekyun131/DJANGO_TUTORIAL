from rest_framework import viewsets

from users.models import Profile
from .models import Post, Comment
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer

from django_filters.rest_framework import DjangoFilterBackend   # view마다 필터 설정할 때 사용

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




# Create your views here.
class PostViewSet(viewsets.ModelViewSet):   # viewsets.ModelViewSet: RESTful API의 대부분을 자동으로 처리
                                            # list(), retrieve(), create(), update(), destroy() 메서드를 제공
    queryset=Post.objects.all()
    permission_classes=[CustomReadOnly]
    filter_backends=[DjangoFilterBackend]   # URL에서 특정 필드를 기준으로 검색이나 필터링이 가능
    filterset_fields=['author', 'likes']
    
    
    def get_serializer_class(self):
        # if self.action=='list' or 'retrieve': # 항상 참이 되는 코드
        if self.action in ['list', 'retrieve']: # 목록 조회나 상세 조회
            return PostSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)
        

# 좋아요  기능
@api_view(['GET'])  # DRF 방식의 API 뷰
@permission_classes([IsAuthenticated])      # 로그인한 사용자만 사용
def like_post(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)     # 이미 좋아요 했으면 취소
    else:
        post.likes.add(request.user)        # 안 했으면 좋아요 추가
        
    return Response({'status':'ok'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    permission_classes=[CustomReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['list' , 'retrieve']:
            return CommentSerializer
        return CommentCreateSerializer
    
    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)