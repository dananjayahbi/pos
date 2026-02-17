"""
LankaCommerce Cloud - Database Router for Cross-Schema Relation Prevention.

This module provides TenantRouter, a custom Django database router that
prevents foreign key relationships between models in different schema
classifications (shared-only vs tenant-only).

Why this is needed:
    django-tenants' TenantSyncRouter only handles migration routing
    (allow_migrate). It does not enforce relation rules between apps
    in different schemas. Without TenantRouter, Django would silently
    allow FK declarations between shared-only and tenant-only models,
    which would fail at runtime because PostgreSQL foreign keys cannot
    span schemas when search_path is set to a single tenant schema.

How it works:
    The router classifies each model's app into one of three categories:
        - shared_only: App is in SHARED_APPS but NOT in TENANT_APPS
        - tenant_only: App is in TENANT_APPS but NOT in SHARED_APPS
        - dual: App is in BOTH lists (e.g. contenttypes, auth)

    Relations between models in the same category (or involving a dual
    app) are allowed. Relations between shared_only and tenant_only
    models are blocked.

Router stack (DATABASE_ROUTERS order):
    1. apps.tenants.routers.TenantRouter  — allow_relation enforcement
    2. django_tenants.routers.TenantSyncRouter — allow_migrate routing

Configuration:
    DATABASE_ROUTERS is defined in config/settings/database.py.

Related documentation:
    - docs/database/database-routers.md
    - docs/database/app-classification.md
"""

from django.conf import settings


def _get_app_classification(app_label):
    """
    Classify an app as 'shared_only', 'tenant_only', or 'dual'.

    Uses SHARED_APPS and TENANT_APPS from settings to determine the
    classification. Apps in both lists are 'dual'. Apps in neither
    list default to 'shared_only' (safe default for unknown apps).

    Parameters
    ----------
    app_label : str
        The Django app label (e.g. 'tenants', 'products', 'auth').

    Returns
    -------
    str
        One of 'shared_only', 'tenant_only', or 'dual'.
    """
    shared_apps = getattr(settings, "SHARED_APPS", [])
    tenant_apps = getattr(settings, "TENANT_APPS", [])

    # Normalize: app labels in settings may use dotted paths
    # (e.g. 'django.contrib.auth'), so extract the last segment
    # for comparison. But also check the full path.
    in_shared = any(
        app_label == app or app.endswith(f".{app_label}")
        for app in shared_apps
    )
    in_tenant = any(
        app_label == app or app.endswith(f".{app_label}")
        for app in tenant_apps
    )

    if in_shared and in_tenant:
        return "dual"
    if in_tenant:
        return "tenant_only"
    # Default: shared_only (safe fallback for framework/unknown apps)
    return "shared_only"


class TenantRouter:
    """
    Custom database router that prevents cross-schema foreign key relations.

    This router only implements allow_relation. All other routing methods
    (db_for_read, db_for_write, allow_migrate) return None, deferring to
    the next router in the stack (TenantSyncRouter).

    Classification rules:
        - shared_only ↔ shared_only: ALLOWED (both in public schema)
        - tenant_only ↔ tenant_only: ALLOWED (both in tenant schema)
        - dual ↔ anything: ALLOWED (dual apps exist in both schemas)
        - shared_only ↔ tenant_only: BLOCKED (cross-schema FK)

    This router is registered first in DATABASE_ROUTERS so that relation
    checks are enforced before TenantSyncRouter processes the request.
    """

    def db_for_read(self, model, **hints):
        """
        Defer read routing to the next router.

        django-tenants handles read routing via PostgreSQL search_path,
        so no router-level routing is needed.
        """
        return None

    def db_for_write(self, model, **hints):
        """
        Defer write routing to the next router.

        django-tenants handles write routing via PostgreSQL search_path,
        so no router-level routing is needed.
        """
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Prevent foreign key relations between shared-only and tenant-only apps.

        Parameters
        ----------
        obj1 : Model instance
            The first model in the proposed relation.
        obj2 : Model instance
            The second model in the proposed relation.
        **hints : dict
            Additional hints (unused).

        Returns
        -------
        bool or None
            True if the relation is allowed, False if blocked,
            None to defer to the next router.
        """
        classification1 = _get_app_classification(obj1._meta.app_label)
        classification2 = _get_app_classification(obj2._meta.app_label)

        # If either model is in a dual app, allow the relation.
        # Dual apps (contenttypes, auth) have tables in both schemas.
        if classification1 == "dual" or classification2 == "dual":
            return True

        # If both models are in the same classification, allow.
        if classification1 == classification2:
            return True

        # Cross-schema relation: shared_only ↔ tenant_only — block it.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Defer migration routing to TenantSyncRouter.

        TenantSyncRouter handles all migration routing logic. This router
        does not interfere with migration behavior.
        """
        return None
