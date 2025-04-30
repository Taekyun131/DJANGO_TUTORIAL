from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI, BooksAPIMixins, BookAPIMixins


urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),               # 함수형 뷰의 booksAPI 연결
    path("fbv/book/<int:bid>/", bookAPI),       # 함수형 뷰의 bookAPI 연결
    path("cbv/books/", BooksAPI.as_view()),             # 클래스형 뷰의 BooksAPI 연결          
    path("cbv/book/<int:bid>/", BookAPI.as_view()),     # 클래스형 뷰의 BookAPI 연결
    path("mixin/books/", BooksAPIMixins.as_view()),             # Mixins를 사용한 BooksAPIMixins 연결
    path("mixin/book/<int:bid>/", BookAPIMixins.as_view()),     # Mixins를 사용한 BookAPIMixins 연결
]

# 라우터 사용
# 라우터를 통해 URL을 일일이 지정하지 않아도 일정한 규칙의 URL 생성가능
from rest_framework import routers
from .views import BookViewSet

router=routers.SimpleRouter()
router.register('books', BookViewSet)

urlpatterns=router.urls