"""
LankaCommerce Cloud - Tenants Admin Configuration.

Registers Tenant and Domain models in Django admin for platform
administrators to manage tenants and their domain mappings.

Admin visibility:
    - Only superusers and platform administrators should have access
      to tenant management. These models live in the public schema.
    - TenantAdmin displays tenant identity, status, billing, and
      schema information.
    - DomainAdmin displays domain-to-tenant mapping and primary status.

Security note:
    - Tenant and Domain admin operates on the public schema only.
    - Business data (products, sales, etc.) is in tenant schemas and
      is NOT accessible through this admin interface.
    - Schema creation/deletion triggers are controlled by
      AUTO_CREATE_SCHEMA and AUTO_DROP_SCHEMA settings.
"""

from django.contrib import admin

from apps.tenants.models import Domain, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tenants.

    Provides list view with key tenant fields, search, and filtering.
    Schema name is read-only because it is auto-generated from the slug
    and should not be changed after creation (changing it would orphan
    the PostgreSQL schema).
    """

    list_display = [
        "name",
        "slug",
        "schema_name",
        "status",
        "on_trial",
        "paid_until",
        "created_on",
    ]
    list_filter = [
        "status",
        "on_trial",
    ]
    search_fields = [
        "name",
        "slug",
        "schema_name",
    ]
    readonly_fields = [
        "schema_name",
        "created_on",
        "updated_on",
    ]
    ordering = ["name"]
    list_per_page = 25

    fieldsets = [
        (
            "Identity",
            {
                "fields": ["name", "slug", "schema_name"],
            },
        ),
        (
            "Billing & Subscription",
            {
                "fields": ["paid_until", "on_trial"],
            },
        ),
        (
            "Lifecycle",
            {
                "fields": ["status"],
            },
        ),
        (
            "Configuration",
            {
                "fields": ["settings"],
                "classes": ["collapse"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_on", "updated_on"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tenant domains.

    Each domain maps a hostname or subdomain to a tenant. The primary
    domain is used for canonical URL generation. TenantMainMiddleware
    uses domain lookups to resolve the current tenant from the Host header.
    """

    list_display = [
        "domain",
        "tenant",
        "is_primary",
    ]
    list_filter = [
        "is_primary",
    ]
    search_fields = [
        "domain",
        "tenant__name",
        "tenant__slug",
    ]
    ordering = ["domain"]
    list_per_page = 25
    raw_id_fields = ["tenant"]
