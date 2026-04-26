"""Permission classes for platform admin API endpoints."""

from rest_framework.permissions import BasePermission


class IsPlatformUser(BasePermission):
    """
    Allows access only to authenticated PlatformUser instances.
    Rejects tenant users (who are regular Django auth.User instances).
    """

    message = "Platform admin access required."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # PlatformUser has an 'is_super_admin' property
        # Regular tenant users don't have this
        return hasattr(user, "is_super_admin")


class IsSuperAdmin(IsPlatformUser):
    """Only super_admin role can access."""

    message = "Super admin access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, "role", None) == "super_admin"


class IsPlatformAdminOrAbove(IsPlatformUser):
    """platform_admin or super_admin can access."""

    message = "Platform admin or super admin access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, "role", None) in ("super_admin", "platform_admin")


class IsSupportOrAbove(IsPlatformUser):
    """support, platform_admin, or super_admin can access."""

    message = "Platform staff access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, "role", None) in (
            "super_admin", "platform_admin", "support"
        )


class IsViewerOrAbove(IsPlatformUser):
    """Any authenticated PlatformUser can access (read-only endpoints)."""

    message = "Platform viewer access required."

    def has_permission(self, request, view):
        return super().has_permission(request, view)
