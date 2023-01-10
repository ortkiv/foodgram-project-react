from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Кастомный пермишен.
    Разрешает просмотр списка подписок его владельцу.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated  # Допилить хозяина
