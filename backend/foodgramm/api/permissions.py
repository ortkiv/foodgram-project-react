from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(permissions.BasePermission):
    """Кастомный пермишен.
    Разрешает просмотр списка подписок его владельцу.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated  # Допилить хозяина


class IsAuthor(permissions.BasePermission):
    """Кастомный пермишен.
    Разрешает измение и удаление обьекта только его автору.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author
