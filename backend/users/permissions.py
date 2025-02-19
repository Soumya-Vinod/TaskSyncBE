from rest_framework import permissions

class IsAdminOrPartialAdmin(permissions.BasePermission):
    """Custom permission to allow only Admins or Partial Admins to modify users."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'partial_admin']
