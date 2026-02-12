"""
URL configuration for LankaCommerce Cloud.

Root URL configuration with organized sections for admin, API, and health checks.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path  # noqa: F401

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
    # Health Checks
    # ──────────────────────────────────────────────
    path("health/", include("apps.core.urls")),
]
