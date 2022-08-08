from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.has_role("admin"):
            return True
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_role("admin"):
            return True
        return False


class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.user == obj or request.user.has_role("admin"):
            return True
        return False
