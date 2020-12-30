from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    # Custom permission class which allow object owner to do all http methods
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
