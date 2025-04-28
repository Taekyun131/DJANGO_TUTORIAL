from django.db import models

# Create your models here.
class Todo(models.Model):
    # Django가 기본으로 제공하는 pk인 id 필드 포함
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)     # 생성일 자동추가
    complete=models.BooleanField(default=False)
    important=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title