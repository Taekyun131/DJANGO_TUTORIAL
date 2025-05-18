from rest_framework import viewsets

from users.models import Profile
from .models import Post
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):   # viewsets.ModelViewSet: RESTful API의 대부분을 자동으로 처리
                                            # list(), retrieve(), create(), update(), destroy() 메서드를 제공
    queryset=Post.objects.all()
    permission_classes=[CustomReadOnly]
    
    def get_serializer_class(self):
        # if self.action=='list' or 'retrieve': # 항상 참이 되는 코드
        if self.action in ['list', 'retrieve']:
            return PostSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)