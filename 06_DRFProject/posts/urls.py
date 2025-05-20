from django.urls import path
from rest_framework import routers

from .views import PostViewSet, like_post, CommentViewSet


router=routers.SimpleRouter()   # root API view 없이 기본적인 URL만 만들어줌
router.register('posts', PostViewSet)   # 'posts'라는 prefix(URL 경로)를 기준으로 PostViewSet을 등록
router.register('comments', CommentViewSet)
urlpatterns=router.urls+[    # 라우터가 자동 생성한 URL 목록을 urlpatterns에 그대로 할당
    path('like/<int:pk>/', like_post, name='like_post')    
]    