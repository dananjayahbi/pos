"""URL patterns for tenant registration and management."""

from django.urls import path

from apps.tenants.views import (
    TenantRegistrationView,
    TenantSlugAvailabilityView,
)

app_name = "tenants"

urlpatterns = [
    # Public: check slug availability (used by registration wizard)
    path(
        "check-slug/",
        TenantSlugAvailabilityView.as_view(),
        name="check-slug",
    ),
    # Public: register a new tenant (business owner self-registration)
    path(
        "register/",
        TenantRegistrationView.as_view(),
        name="register",
    ),
]
