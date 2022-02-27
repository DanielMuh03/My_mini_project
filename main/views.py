from datetime import timedelta
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .permissions import *
from rest_framework.renderers import JSONRenderer


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostsView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('week', 0))
        if weeks_count > 0:
            start_data = timezone.now() - timedelta(weeks=weeks_count)
            queryset = queryset.filter(created_at__gte=start_data)
        return queryset

    @action(detail=False, methods=['POST'])
    def comment(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = MusicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        serializer = MusicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        user = request.user
        reply = get_object_or_404(Music, pk=pk)
        if user.is_authenticated:
            if user in reply.likes.all():
                reply.likes.remove(user)
                message = 'Unliked!'
            else:
                reply.likes.add(user)
                message = 'liked'
        context = {'status': message}
        return Response(context, status=200)


class MusicImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = MusicImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

