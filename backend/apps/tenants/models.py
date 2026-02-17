"""
LankaCommerce Cloud - Tenant and Domain Models.

Defines the Tenant and Domain models for multi-tenant SaaS operations.

The Tenant model represents an organization (business) in the platform.
Each tenant maps to a dedicated PostgreSQL schema where all tenant-specific
business data (products, sales, inventory, etc.) is stored in isolation.

The Domain model maps hostnames and subdomains to tenants. django-tenants
uses this mapping to resolve the current tenant from the incoming request
hostname via TenantMainMiddleware, which then sets the PostgreSQL
search_path to the tenant's schema.

The Tenant model extends django-tenants' TenantMixin, which provides the
schema_name field and schema lifecycle management (auto-create on save,
optional auto-drop on delete).

Key fields:
    - schema_name: PostgreSQL schema name (from TenantMixin, e.g. 'tenant_acme')
    - name: Human-readable business name
    - slug: URL-safe identifier used in subdomains and schema naming
    - paid_until: Subscription expiry date for billing lifecycle
    - on_trial: Whether the tenant is currently on a trial period
    - status: Lifecycle state (active, suspended, archived)
    - settings: Per-tenant JSON configuration
    - created_on / updated_on: Audit timestamps

Related models (defined in this same module):
    - Domain: Maps hostnames/subdomains to tenants (see 02_Tasks-49-52)

Settings references:
    - TENANT_MODEL = "tenants.Tenant" (in config/settings/database.py)
    - TENANT_SCHEMA_PREFIX = "tenant_" (in config/settings/database.py)
    - AUTO_CREATE_SCHEMA = True (schema created on Tenant.save())
    - AUTO_DROP_SCHEMA = False (schema NOT dropped on Tenant.delete())
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_tenants.models import DomainMixin, TenantMixin


# ════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════

# Tenant lifecycle statuses
TENANT_STATUS_ACTIVE = "active"
TENANT_STATUS_SUSPENDED = "suspended"
TENANT_STATUS_ARCHIVED = "archived"

TENANT_STATUS_CHOICES = [
    (TENANT_STATUS_ACTIVE, "Active"),
    (TENANT_STATUS_SUSPENDED, "Suspended"),
    (TENANT_STATUS_ARCHIVED, "Archived"),
]

# Schema name reserved words that cannot be used as tenant slugs
RESERVED_SCHEMA_NAMES = frozenset({
    "public",
    "pg_catalog",
    "information_schema",
    "pg_toast",
})

# Slug validation regex: lowercase letters, digits, and hyphens.
# Must start with a letter or digit. No consecutive hyphens.
SLUG_REGEX = r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9]))*$"

# Default per-tenant settings structure
DEFAULT_TENANT_SETTINGS = {
    "currency": "LKR",
    "timezone": "Asia/Colombo",
    "date_format": "YYYY-MM-DD",
    "language": "en",
}


# ════════════════════════════════════════════════════════════════════════
# VALIDATORS
# ════════════════════════════════════════════════════════════════════════

slug_validator = RegexValidator(
    regex=SLUG_REGEX,
    message=(
        "Slug must contain only lowercase letters, digits, and hyphens. "
        "Must start with a letter or digit. No consecutive hyphens."
    ),
)


# ════════════════════════════════════════════════════════════════════════
# TENANT MODEL
# ════════════════════════════════════════════════════════════════════════

class Tenant(TenantMixin):
    """
    Represents a tenant (business organization) in LankaCommerce Cloud.

    Each Tenant instance corresponds to a PostgreSQL schema that isolates
    all business data (products, sales, inventory, customers, etc.) from
    other tenants. The public tenant (schema_name='public') hosts shared
    platform data.

    TenantMixin provides:
        - schema_name (CharField, max_length=63, unique): The PostgreSQL
          schema name. Set to 'public' for the shared/public tenant, or
          'tenant_<slug>' for business tenants.
        - auto_create_schema (bool): When True, saving a new instance
          creates the schema and runs TENANT_APPS migrations.
        - auto_drop_schema (bool): When True, deleting the instance drops
          the schema. MUST remain False in production.

    LankaCommerce adds:
        - name: Human-readable business name
        - slug: URL-safe identifier for subdomains and schema naming
        - paid_until: Subscription expiry for billing lifecycle
        - on_trial: Trial period flag
        - status: Lifecycle state management
        - settings: Per-tenant JSON configuration
        - created_on / updated_on: Audit timestamps
    """

    # ── Core Identity ───────────────────────────────────────────────
    name = models.CharField(
        max_length=255,
        help_text="Human-readable business name (e.g. 'Acme Trading Pvt Ltd').",
    )

    slug = models.SlugField(
        max_length=63,
        unique=True,
        validators=[slug_validator],
        help_text=(
            "URL-safe tenant identifier used in subdomains and schema naming. "
            "Lowercase letters, digits, and hyphens only. "
            "Example: 'acme-trading' -> schema 'tenant_acme_trading', "
            "subdomain 'acme-trading.lankacommerce.lk'."
        ),
    )

    # ── Billing & Subscription ──────────────────────────────────────
    paid_until = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "Subscription expiry date. Null for the public tenant or "
            "tenants with unlimited access. After this date, the tenant "
            "may be suspended or moved to a limited plan."
        ),
    )

    on_trial = models.BooleanField(
        default=True,
        help_text=(
            "Whether this tenant is currently on a trial period. "
            "Trial tenants may have feature restrictions."
        ),
    )

    # ── Lifecycle Status ────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=TENANT_STATUS_CHOICES,
        default=TENANT_STATUS_ACTIVE,
        db_index=True,
        help_text=(
            "Tenant lifecycle state. "
            "'active': fully operational. "
            "'suspended': temporarily disabled (e.g. payment overdue). "
            "'archived': permanently deactivated, data retained for compliance."
        ),
    )

    # ── Per-Tenant Settings ─────────────────────────────────────────
    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Per-tenant configuration stored as JSON. "
            "Expected keys: currency, timezone, date_format, language. "
            "Defaults are applied at the application layer if keys are missing."
        ),
    )

    # ── Timestamps ──────────────────────────────────────────────────
    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When this tenant was created.",
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="When this tenant was last updated.",
    )

    # ── Schema Lifecycle (from TenantMixin) ─────────────────────────
    # auto_create_schema is inherited from TenantMixin.
    # Default is True (set in database.py as AUTO_CREATE_SCHEMA).
    # When True, saving a new Tenant creates the PostgreSQL schema
    # and runs all TENANT_APPS migrations in it.
    auto_create_schema = True

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validate tenant fields before saving.

        Ensures:
            1. Slug is not a reserved PostgreSQL schema name (except
               the public tenant, which is allowed to use 'public')
            2. Schema name follows the tenant_<slug> convention
            3. Schema name does not exceed PostgreSQL's 63-char limit
        """
        super().clean()

        # The public tenant (schema_name='public') is exempt from
        # reserved-name validation because it is a required system tenant.
        is_public_tenant = self.schema_name == "public"

        # Validate slug is not a reserved name (skip for public tenant)
        if (
            self.slug
            and self.slug.lower() in RESERVED_SCHEMA_NAMES
            and not is_public_tenant
        ):
            raise ValidationError({
                "slug": f"'{self.slug}' is a reserved name and cannot be used as a tenant slug.",
            })

        # If schema_name is not yet set and slug is available, generate it
        # (public tenant already has schema_name='public', so this is skipped)
        if self.slug and not self.schema_name:
            prefix = getattr(settings, "TENANT_SCHEMA_PREFIX", "tenant_")
            self.schema_name = f"{prefix}{self.slug.replace('-', '_')}"

        # Validate schema_name length (PostgreSQL limit: 63 characters)
        if self.schema_name and len(self.schema_name) > 63:
            raise ValidationError({
                "slug": (
                    f"Generated schema name '{self.schema_name}' exceeds "
                    "PostgreSQL's 63-character limit. Use a shorter slug."
                ),
            })

    def save(self, *args, **kwargs):
        """
        Save the tenant, auto-generating schema_name from slug if needed.

        The public tenant (schema_name='public') skips schema name generation.
        Business tenants get schema_name = tenant_<slug> with hyphens
        converted to underscores for PostgreSQL compatibility.
        """
        # Auto-generate schema_name from slug for non-public tenants
        if self.slug and not self.schema_name:
            prefix = getattr(settings, "TENANT_SCHEMA_PREFIX", "tenant_")
            self.schema_name = f"{prefix}{self.slug.replace('-', '_')}"

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """Return True if the tenant is in active status."""
        return self.status == TENANT_STATUS_ACTIVE

    @property
    def is_suspended(self):
        """Return True if the tenant is suspended."""
        return self.status == TENANT_STATUS_SUSPENDED

    @property
    def is_archived(self):
        """Return True if the tenant is archived."""
        return self.status == TENANT_STATUS_ARCHIVED

    @property
    def is_paid(self):
        """Return True if the tenant's subscription has not expired."""
        if self.paid_until is None:
            return True  # No expiry date means unlimited access
        return self.paid_until >= timezone.now().date()

    @property
    def is_public(self):
        """Return True if this is the public (shared) tenant."""
        return self.schema_name == "public"

    def get_setting(self, key, default=None):
        """
        Retrieve a per-tenant setting value.

        Falls back to DEFAULT_TENANT_SETTINGS if the key is not set,
        then to the provided default.
        """
        if self.settings and key in self.settings:
            return self.settings[key]
        return DEFAULT_TENANT_SETTINGS.get(key, default)


# ════════════════════════════════════════════════════════════════════════
# DOMAIN MODEL
# ════════════════════════════════════════════════════════════════════════

class Domain(DomainMixin):
    """
    Maps hostnames and subdomains to tenants for request routing.

    django-tenants uses the Domain model to resolve which tenant a request
    belongs to. When a request arrives, TenantMainMiddleware looks up the
    Host header in the Domain table and activates the corresponding
    tenant's PostgreSQL schema.

    DomainMixin provides:
        - domain (CharField, max_length=253, unique): The hostname or
          subdomain that maps to a tenant. Must not include port numbers
          or 'www' prefix. Examples: 'acme.lankacommerce.lk', 'localhost'.
        - tenant (ForeignKey to TENANT_MODEL, related_name='domains'):
          The tenant this domain belongs to. Each domain belongs to
          exactly one tenant, but a tenant can have multiple domains.
        - is_primary (BooleanField, default=True): Whether this is the
          primary domain for the tenant. Only one domain per tenant
          should be marked as primary. The primary domain is used for
          generating canonical URLs and redirects.

    Domain routing examples:
        - Public tenant:   domain='localhost'              -> schema: public
        - Public tenant:   domain='lankacommerce.lk'       -> schema: public
        - Business tenant:  domain='acme.lankacommerce.lk'  -> schema: tenant_acme
        - Business tenant:  domain='acme.localhost'          -> schema: tenant_acme

    Settings references:
        - TENANT_DOMAIN_MODEL = "tenants.Domain" (in config/settings/database.py)
        - BASE_TENANT_DOMAIN configured per environment (.env.docker)
    """

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"
        ordering = ["domain"]

    def __str__(self):
        return self.domain
