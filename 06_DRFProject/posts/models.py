from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile
# Create your models here.

class Post(models.Model):
    # related_name='posts': user.posts.all()처럼 사용자가 쓴 글들 조회 가능
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title=models.CharField(max_length=128)
    category=models.CharField(max_length=128)
    body=models.TextField()
    image=models.ImageField(upload_to='post/', default='default.png')
    # related_name='like_posts': user.like_posts.all() 처럼 사용자가 좋아요한 글 목록 조회 가능
    likes=models.ManyToManyField(User, related_name='like_posts', blank=True)
    published_date=models.DateTimeField(default=timezone.now)