# 시리얼라이즈&디시리얼라이즈
# 클라이언트와 서버가 통신할 때, 주고받는 데이터의 형식이 python객체와 json으로 서로 다르기 때문에 변환하는 작업 필요

from rest_framework import serializers
from .models import Book

# class BookSerializer(serializers.Serializer):
#     bid=serializers.IntegerField(primary_key=True)
#     title=serializers.CharField(max_length=50)
#     author=serializers.CharField(max_length=50)
#     category=serializers.CharField(max_length=50)
#     pages=serializers.IntegerField()
#     price=serializers.IntegerField()
#     published_date=serializers.DateField()
#     description=serializers.TextField()
    
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.bid=validated_data.get('bid', instance.bid)
#         instance.title=validated_data.get('title', instance.title)
#         instance.author=validated_data.get('author', instance.author)
#         instance.category=validated_data.get('category', instance.category)
#         instance.pages=validated_data.get('pages', instance.pages)
#         instance.price=validated_data.get('price', instance.price)
#         instance.published_date=validated_data.get('published_date', instance.published_date)
#         instance.description=validated_data.get('description', instance.description)
#         instance.save()
#         return instance


# 모델 기반으로 동작하는 시리얼라이저
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['bid', 'title', 'author', 'category', 'pages', 'price', 'published_date', 'description']