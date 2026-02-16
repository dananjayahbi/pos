"""
URL configuration for LankaCommerce Cloud.

Root URL configuration with organized sections for admin, API, and health checks.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path  # noqa: F401
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ──────────────────────────────────────────────
    # Admin
    # ──────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ──────────────────────────────────────────────
    # API v1 (to be added with DRF)
    # ──────────────────────────────────────────────
    # path("api/v1/auth/", include("apps.authentication.urls")),
    # path("api/v1/tenants/", include("apps.tenants.urls")),
    # path("api/v1/inventory/", include("apps.inventory.urls")),
    # path("api/v1/pos/", include("apps.pos.urls")),

    # ──────────────────────────────────────────────
    # API Documentation — drf-spectacular
    # ──────────────────────────────────────────────
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # ──────────────────────────────────────────────
    # Health Checks
    # ──────────────────────────────────────────────
    path("health/", include("apps.core.urls")),
]
