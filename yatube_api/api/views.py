from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets

from posts.models import Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          GroupSerializer, PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки API к модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки API к модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки API к модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
