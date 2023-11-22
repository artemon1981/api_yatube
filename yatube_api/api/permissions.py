from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс пользовательского permission."""

    def has_object_permission(self, request, view, obj):
        """Проверка доступности объекта пользователю."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
