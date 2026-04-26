"""Tenant-aware cache key function for Redis."""

from django.db import connection


def tenant_cache_key(key: str, key_prefix: str, version: int) -> str:
    """
    Generate a cache key prefixed with the current tenant schema name.
    This ensures cache isolation between tenants.

    Format: {schema_name}:{key_prefix}:{version}:{key}
             or {schema_name}:{version}:{key} when key_prefix is empty.

    Used as the KEY_FUNCTION for the "default" Django cache backend.
    The schema_name is read from django-tenants' connection attribute,
    which is set by LCCTenantMiddleware for every HTTP request.

    For Celery tasks, ensure schema_context() is active before any
    cache.get/set call so the correct prefix is used.
    """
    schema_name = getattr(connection, "schema_name", "public")
    if key_prefix:
        return f"{schema_name}:{key_prefix}:{version}:{key}"
    return f"{schema_name}:{version}:{key}"
