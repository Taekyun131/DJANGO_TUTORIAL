from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  # 객체가 저장된 직후에 작동하는 시그널.
from django.dispatch import receiver    # 시그널을 연결하는 데코레이터.

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # primary key를 User의 pk로 설정하여 통합적으로 관리
    nickname=models.CharField(max_length=128)
    position=models.CharField(max_length=128)
    subjects=models.CharField(max_length=128)
    image=models.ImageField(upload_to='profile/', default='default.png')

# User 객체가 새로 생성된 후(post_save) 실행되는 함수
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)