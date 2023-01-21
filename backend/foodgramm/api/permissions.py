from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if self.has_permission(request, view):
            return True
        return (
            request.user.is_authenticated and
            (request.user == obj.author or request.user.is_superuser)
        )
