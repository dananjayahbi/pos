"""
Platform management API views.
All views require PlatformUser authentication.
Tenant data is read from the public schema (Tenant model).
"""

import logging
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.permissions import (
    IsPlatformAdminOrAbove,
    IsSuperAdmin,
    IsSupportOrAbove,
)
from apps.platform.serializers import (
    PlatformUserCreateSerializer,
    PlatformUserListSerializer,
    PlatformUserUpdateSerializer,
    SubscriptionPlanSerializer,
    TenantDetailSerializer,
    TenantListSerializer,
    TenantStatusUpdateSerializer,
)
from apps.tenants.models import Tenant

logger = logging.getLogger(__name__)


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


# ─── Tenant Management ────────────────────────────────────────────────────────

class TenantListView(APIView):
    """
    GET /api/v1/platform/tenants/
    List all tenants with optional filters.
    Access: platform_admin, super_admin
    """

    permission_classes = [IsPlatformAdminOrAbove]

    def get(self, request):
        queryset = Tenant.objects.exclude(schema_name="public").order_by("-created_on")

        # Filters
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        on_trial = request.query_params.get("on_trial")
        if on_trial is not None:
            queryset = queryset.filter(on_trial=on_trial.lower() == "true")

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search) | Tenant.objects.filter(
                contact_email__icontains=search
            ).exclude(schema_name="public")

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TenantListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TenantDetailView(APIView):
    """
    GET /api/v1/platform/tenants/{schema_name}/
    Get full details of a specific tenant.
    Access: support, platform_admin, super_admin
    """

    permission_classes = [IsSupportOrAbove]

    def get(self, request, schema_name):
        tenant = get_object_or_404(Tenant, schema_name=schema_name)
        serializer = TenantDetailSerializer(tenant)
        return Response(serializer.data)


class TenantStatusView(APIView):
    """
    POST /api/v1/platform/tenants/{schema_name}/set-status/
    Change a tenant's status (suspend, reactivate, archive).
    Access: platform_admin, super_admin
    """

    permission_classes = [IsPlatformAdminOrAbove]

    def post(self, request, schema_name):
        tenant = get_object_or_404(Tenant, schema_name=schema_name)

        serializer = TenantStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]
        old_status = tenant.status

        tenant.status = new_status
        tenant.save(update_fields=["status"])

        logger.info(
            "Tenant %s status changed from %s to %s by platform user %s",
            schema_name,
            old_status,
            new_status,
            request.user.email,
        )

        return Response({
            "schema_name": tenant.schema_name,
            "name": tenant.name,
            "old_status": old_status,
            "new_status": new_status,
            "message": f"Tenant '{tenant.name}' status updated to '{new_status}'.",
        })


class TenantSuspendView(APIView):
    """
    POST /api/v1/platform/tenants/{schema_name}/suspend/
    Convenience endpoint to suspend a tenant.
    Access: platform_admin, super_admin
    """

    permission_classes = [IsPlatformAdminOrAbove]

    def post(self, request, schema_name):
        tenant = get_object_or_404(Tenant, schema_name=schema_name)
        if tenant.status == "suspended":
            return Response({"detail": "Tenant is already suspended."}, status=400)
        tenant.status = "suspended"
        tenant.save(update_fields=["status"])
        logger.info("Tenant %s suspended by %s", schema_name, request.user.email)
        return Response({"message": f"Tenant '{tenant.name}' has been suspended."})


class TenantReactivateView(APIView):
    """
    POST /api/v1/platform/tenants/{schema_name}/reactivate/
    Reactivate a suspended tenant.
    Access: platform_admin, super_admin
    """

    permission_classes = [IsPlatformAdminOrAbove]

    def post(self, request, schema_name):
        tenant = get_object_or_404(Tenant, schema_name=schema_name)
        if tenant.status == "active":
            return Response({"detail": "Tenant is already active."}, status=400)
        tenant.status = "active"
        tenant.save(update_fields=["status"])
        logger.info("Tenant %s reactivated by %s", schema_name, request.user.email)
        return Response({"message": f"Tenant '{tenant.name}' has been reactivated."})


class TenantExtendTrialView(APIView):
    """
    POST /api/v1/platform/tenants/{schema_name}/extend-trial/
    Extend a tenant's trial period.
    Body: {"days": 7}
    Access: super_admin only
    """

    permission_classes = [IsSuperAdmin]

    def post(self, request, schema_name):
        tenant = get_object_or_404(Tenant, schema_name=schema_name)
        days = int(request.data.get("days", 7))
        if days < 1 or days > 90:
            return Response({"error": "Days must be between 1 and 90."}, status=400)

        base = max(tenant.paid_until, timezone.now().date()) if tenant.paid_until else timezone.now().date()
        tenant.paid_until = base + timedelta(days=days)
        tenant.on_trial = True
        tenant.save(update_fields=["paid_until", "on_trial"])

        return Response({
            "message": f"Trial extended by {days} days.",
            "new_paid_until": tenant.paid_until.isoformat(),
        })


# ─── Platform User Management ─────────────────────────────────────────────────

from apps.platform.models import PlatformUser  # noqa: E402


class PlatformUserListView(APIView):
    """
    GET  /api/v1/platform/users/   — list platform staff
    POST /api/v1/platform/users/   — create platform staff
    Access: GET → support+, POST → super_admin only
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSuperAdmin()]
        return [IsSupportOrAbove()]

    def get(self, request):
        users = PlatformUser.objects.all().order_by("email")

        # Non-super-admin staff can't see other super_admins
        if getattr(request.user, "role", None) != "super_admin":
            users = users.exclude(role="super_admin")

        serializer = PlatformUserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlatformUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Only super_admin can create another super_admin
        role = serializer.validated_data.get("role", "platform_admin")
        if role == "super_admin" and not getattr(request.user, "is_super_admin", False):
            return Response(
                {"error": "Only a super admin can create another super admin."},
                status=403,
            )

        user = serializer.save()
        logger.info("Platform user created: %s (role=%s) by %s", user.email, user.role, request.user.email)

        return Response(
            PlatformUserListSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class PlatformUserDetailView(APIView):
    """
    GET    /api/v1/platform/users/{id}/  — get platform staff detail
    PATCH  /api/v1/platform/users/{id}/  — update platform staff
    DELETE /api/v1/platform/users/{id}/  — deactivate platform staff
    Access: super_admin (write), support+ (read)
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsSupportOrAbove()]
        return [IsSuperAdmin()]

    def get(self, request, user_id):
        user = get_object_or_404(PlatformUser, id=user_id)
        return Response(PlatformUserListSerializer(user).data)

    def patch(self, request, user_id):
        user = get_object_or_404(PlatformUser, id=user_id)

        # Can't modify yourself
        if str(user.id) == str(request.user.id):
            return Response({"error": "You cannot modify your own account."}, status=400)

        serializer = PlatformUserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("Platform user %s updated by %s", user.email, request.user.email)
        return Response(PlatformUserListSerializer(user).data)

    def delete(self, request, user_id):
        user = get_object_or_404(PlatformUser, id=user_id)

        if str(user.id) == str(request.user.id):
            return Response({"error": "You cannot deactivate your own account."}, status=400)

        # Soft delete (deactivate, don't actually delete)
        user.is_active = False
        user.save(update_fields=["is_active"])

        logger.info("Platform user %s deactivated by %s", user.email, request.user.email)
        return Response({"message": f"Platform user '{user.email}' has been deactivated."})


# ─── Subscription Plans ───────────────────────────────────────────────────────

class SubscriptionPlanListView(APIView):
    """
    GET /api/v1/platform/subscriptions/   — list all plans
    Access: support+
    """

    permission_classes = [IsSupportOrAbove]

    def get(self, request):
        from apps.platform.models import SubscriptionPlan  # noqa: PLC0415

        plans = SubscriptionPlan.objects.filter(is_active=True).order_by("monthly_price")
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)


# ─── Platform Dashboard Stats ─────────────────────────────────────────────────

class PlatformDashboardStatsView(APIView):
    """
    GET /api/v1/platform/stats/
    Returns high-level platform statistics for the dashboard.
    Access: support+
    """

    permission_classes = [IsSupportOrAbove]

    def get(self, request):
        today = timezone.now().date()

        total_tenants = Tenant.objects.exclude(schema_name="public").count()
        active_tenants = Tenant.objects.exclude(schema_name="public").filter(status="active").count()
        suspended_tenants = Tenant.objects.exclude(schema_name="public").filter(status="suspended").count()
        archived_tenants = Tenant.objects.exclude(schema_name="public").filter(status="archived").count()
        on_trial_tenants = Tenant.objects.exclude(schema_name="public").filter(on_trial=True).count()
        trial_expiring_soon = Tenant.objects.exclude(schema_name="public").filter(
            on_trial=True,
            paid_until__gte=today,
            paid_until__lte=today + timedelta(days=3),
        ).count()

        recent_registrations = Tenant.objects.exclude(schema_name="public").filter(
            created_on__date__gte=today - timedelta(days=30)
        ).count()

        return Response({
            "tenants": {
                "total": total_tenants,
                "active": active_tenants,
                "suspended": suspended_tenants,
                "archived": archived_tenants,
                "on_trial": on_trial_tenants,
                "trial_expiring_soon": trial_expiring_soon,
                "recent_registrations_30d": recent_registrations,
            },
        })
