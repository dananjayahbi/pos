"""URL patterns for tenant-scoped self-service domain management."""

from django.urls import path

from apps.tenants.domain_views import (
    TenantDomainDeleteView,
    TenantDomainListView,
    TenantDomainVerifyView,
)

app_name = "tenant-self"

urlpatterns = [
    path("domains/", TenantDomainListView.as_view(), name="domain-list"),
    path("domains/<int:domain_id>/", TenantDomainDeleteView.as_view(), name="domain-delete"),
    path("domains/<int:domain_id>/verify/", TenantDomainVerifyView.as_view(), name="domain-verify"),
]
