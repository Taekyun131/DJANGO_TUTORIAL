# APIVies를 활용해 개발
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
# from django.shortcuts import render

# Create your views here.

class TodosAPIView(APIView):
    # 전체조회
    def get(self, request):
        todos=Todo.objects.filter(complete=False)
        serializer=TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 생성
    def post(self, request):
        serializer=TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class TodoAPIView(APIView):
    # 상세조회
    def get(self, request, pk):
        todo=get_object_or_404(Todo, id=pk)
        serializer=TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 수정
    def put(self, request, pk):
        todo=get_object_or_404(Todo, id=pk)
        serializer=TodoCreateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 완료된 Todo조회
class DoneTodosAPIView(APIView):
    def get(self, request):
        dones=Todo.objects.filter(complete=True)
        serializer=TodoSimpleSerializer(dones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoneTodoAPIView(APIView):
    def get(self, request, pk):
        done=get_object_or_404(Todo, id=pk)
        done.complete=True
        done.save()
        serializer=TodoDetailSerializer(done)
        return Response(status=status.HTTP_200_OK)