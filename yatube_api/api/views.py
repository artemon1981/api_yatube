"""Вью функции api."""
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets

from posts.models import Group, Post
from .serializers import (CommentSerializer,
                          GroupSerializer, PostSerializer)


class AuthUserEditSelfContent(permissions.BasePermission):
    """Класс пользовательского permission."""

    def has_object_permission(self, request, view, obj):
        """Проверка доступности объекта пользователю."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки API к модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки API к модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, AuthUserEditSelfContent]

    def perform_create(self, serializer):
        """Переопределение метода создания."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки API к модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, AuthUserEditSelfContent]

    def get_queryset(self):
        """Переопределение метода получения queryset."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        """Переопределение метода создания."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
