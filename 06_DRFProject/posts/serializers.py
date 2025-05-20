from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    
    class Meta:
        model=Comment
        fields=("pk", "profile", "post", "text")
        

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=("post", "text")

# 게시글 조회용
class PostSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)   # nested serializer
    # 게시글의 작성자 정보를 단순히 ID로 주는 게 아니라, 닉네임, 포지션 등 자세한 프로필 정보도 같이 포함해서 응답에 포함
    
    comments=CommentSerializer(many=True, read_only=True)
    
    class Meta:     # 응답에 포함시킬 모델, 필드정의
        model=Post
        fields=("pk", "profile", "title", "body", "image", "published_date", "likes", "comments")   
        
# 게시글 작성용
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=("title", "category", "body", "image")
        

