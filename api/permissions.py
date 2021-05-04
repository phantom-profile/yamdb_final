from rest_framework import permissions


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS \
            or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.role == request.user.Role.MODERATOR
            or request.user.role == request.user.Role.ADMIN)
