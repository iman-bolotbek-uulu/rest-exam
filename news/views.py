from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets, generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from account.permission import IsAuthorPermission
from . import models
from . import serializers


class NewsPagePagination(PageNumberPagination):
    page_size = 3


class NewsViewSet(viewsets.ModelViewSet):

    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer

    permission_classes = [IsAuthorPermission, ]
    pagination_class = NewsPagePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', ]
    ordering_fields = ['created', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorPermission, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )


class CommentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorPermission, ]
    pagination_class = LimitOffsetPagination


class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [permissions.IsAdminUser, ]


@permission_classes(permissions.IsAuthenticated)
@api_view(['GET'])
def status_news(request, news_id, slug):
    my_status = models.Status.objects.get(slug=slug)
    try:
        models.NewsStatus.objects.create(news_id=news_id, status=my_status, author=request.user.author)
    except:
        return Response({'error': "You already added status"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)


@permission_classes(permissions.IsAuthenticated)
@api_view(['GET'])
def status_comment(request, comment_id, slug):
    my_status = models.Status.objects.get(slug=slug)
    try:
        models.CommentStatus.objects.create(comment_id=comment_id, status=my_status, author=request.user.author)
    except:
        return Response({'error': "You already added status"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)







