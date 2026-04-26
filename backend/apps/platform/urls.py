"""URL patterns for platform admin API."""

from django.urls import path

from apps.platform.auth import PlatformLoginView
from apps.platform.views import (
    PlatformDashboardStatsView,
    PlatformUserDetailView,
    PlatformUserListView,
    SubscriptionPlanListView,
    TenantDetailView,
    TenantExtendTrialView,
    TenantListView,
    TenantReactivateView,
    TenantStatusView,
    TenantSuspendView,
)

app_name = "platform"

urlpatterns = [
    # ── Platform Auth ──────────────────────────────────────────────────────────
    path(
        "auth/login/",
        PlatformLoginView.as_view(),
        name="auth-login",
    ),

    # ── Dashboard Stats ────────────────────────────────────────────────────────
    path(
        "stats/",
        PlatformDashboardStatsView.as_view(),
        name="stats",
    ),

    # ── Tenant Management ──────────────────────────────────────────────────────
    path(
        "tenants/",
        TenantListView.as_view(),
        name="tenant-list",
    ),
    path(
        "tenants/<str:schema_name>/",
        TenantDetailView.as_view(),
        name="tenant-detail",
    ),
    path(
        "tenants/<str:schema_name>/set-status/",
        TenantStatusView.as_view(),
        name="tenant-set-status",
    ),
    path(
        "tenants/<str:schema_name>/suspend/",
        TenantSuspendView.as_view(),
        name="tenant-suspend",
    ),
    path(
        "tenants/<str:schema_name>/reactivate/",
        TenantReactivateView.as_view(),
        name="tenant-reactivate",
    ),
    path(
        "tenants/<str:schema_name>/extend-trial/",
        TenantExtendTrialView.as_view(),
        name="tenant-extend-trial",
    ),

    # ── Platform User Management ───────────────────────────────────────────────
    path(
        "users/",
        PlatformUserListView.as_view(),
        name="user-list",
    ),
    path(
        "users/<uuid:user_id>/",
        PlatformUserDetailView.as_view(),
        name="user-detail",
    ),

    # ── Subscription Plans ─────────────────────────────────────────────────────
    path(
        "subscriptions/",
        SubscriptionPlanListView.as_view(),
        name="subscription-list",
    ),
]
