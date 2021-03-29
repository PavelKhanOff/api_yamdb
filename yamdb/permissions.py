from rest_framework import permissions

from .models import UserRole


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_staff
                     or request.user.role == UserRole.ADMIN))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_staff
                     or request.user.role == 'admin')
                )


class ReviewCommentPermissions(permissions.BasePermission):
    """Права доступа для комментариев и отзывов"""
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()
        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author
                    or request.user.role == UserRole.ADMIN
                    or request.user.role == UserRole.MODERATOR)
        return request.method in permissions.SAFE_METHODS
