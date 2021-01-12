from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import viewsets, filters, generics
from .permissions import ArticlePermission, IsCommentAuthor, IsArticleAuthor

from .models import Article, Comment, Category
from .serializers import ArticleSerializer, CommentSerializer, CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'title', ]
    search_fields = ['title', ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [ArticlePermission, IsArticleAuthor]
        return [permission() for permission in permissions]

class SingleArticleView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ArticlePermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCommentAuthor, ]
        return [permission() for permission in permissions]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer