# 뷰는 크게 함수기반 뷰(Function Based View)와 클래스 기반 뷰(Class Based View)로 분류

# from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework .generics import get_object_or_404 
from .models import Book    
from .serializers import BookSerializer

# Create your views here.
# FBV
@api_view(['GET'])  # 데코레이터: API로 동작하기 위해 코드를 붙임
def HelloAPI(request):
    return Response("hello world!")

# 위 코드를 CBV로 변환하면
# class HelloAPI(APIView):
#     def get(self, request):
#         return Response("hello world")


# FBV로 작성

@api_view(['GET', 'POST'])                  # GET/POST 요청을 처리하게 해주는 데코레이터
def booksAPI(request):
    if request.method=='GET':       # GET 요청(도서 전체 정보)
        books=Book.objects.all()    # Book 모델로부터 전체데이터 가져오기
        serializer=BookSerializer(books, many=True)
        # 시리얼라이저에 전체 데이터를 한 번에 집어넣기(직렬화, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method=='POST':    # POST 요청(도서 정보 등록)
        serializer=BookSerializer(data=request.data)
        # POST 요청으로 들어온 데이터를 시리얼라이저에 집어넣기
        if serializer.is_valid():   # 유효한 데이터 판별
            serializer.save()
            # 시리얼라이저의 역직렬화를 통해 save(), 모델 시리얼라이저의 기본 create() 함수가 동작
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 201 메시지를 보내며 성공
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # 400 잘못된 요청

@api_view(['GET'])
def bookAPI(request, bid):
    book=get_object_or_404(Book, bid=bid)   # bid=bid인 데이터를 Book에서 가져오고, 없으면 404 에러
    serializer=BookSerializer(book)         # 시러얼라이저에 데이터를 집어넣기(직렬화)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
# 위 코드를 CBV로 작성
class BooksAPI(APIView):
    def get(self, request):
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book=get_object_or_404(Book, bid=bid)
        serializer=BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# CBV로 작성된 코드를 mixins를 사용해 리팩터링
# mixins: 공통된 CRUD 기능을 부분적으로 재사용할 수 있도록 도와주는 클래스
from rest_framework import generics
from rest_framework import mixins

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    
    def get(self, request, *args, **kwargs):            # GET 메서드 처리함수(전체목록)
        return self.list(request, *args, **kwargs)      # mixins.ListModelMixin과 연결
    def post(self, request, *args, **kwargs):           # POST 메서드 처리함수(1권 등록)
        return self.create(request, *args, **kwargs)    # mixins.CreateModelMixin과 연결
    
class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    lookup_field='bid'
    # Django 기본모델 pk가 아닌 bid를 pk로 사용하고 있으니 lookup_field로 설정
    
    def get(self, request, *args, **kwargs):                # GET 메서드 처리함수(1권)
        return self.retrieve(request, *args, **kwargs)      # mixins.RetrieveModelMixin과 연결
        
    def put(self, request, *args, **kwargs):                # PUT 메서드 처리함수(1권 수정)
        return self.update(request, *args, **kwargs)        # mixins.UpdateModelMixin과 연결
        
    def delete(self, request, *args, **kwargs):             # DELETE 메서드 처리함수(1권 삭제)
        return self.destroy(request, *args, **kwargs)       # mixins.DestroyModelMixin과 연결
        

# generics 사용해 REST API 구현
# generics: CRUD 기능을 보다 간단하게 구현할 수 있도록 도와주는 기본 클래스
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    
class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    lookup_field='bid'
    

# ModelViewset 사용해 REST API 구현 (Viewset은 mixin을 기반으로 작성됨)
# 하나의 클래스로 하나의 모델에 대한 내용을 전부 작성가능
# 그에 따라 queryset이나 serializer_class 등 겹치는 부분 최소화
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
