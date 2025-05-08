from rest_framework import serializers
from .models import Todo

# 전체조회용 
class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=('id', 'title', 'complete', 'important')
        
# 상세 조회용
class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=('id', 'title', 'description', 'created', 'complete', 'important')
        
# 생성용, 수정용
class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=('title', 'description', 'important')