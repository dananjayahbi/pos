"""Tenant-aware file upload helpers."""

from django.db import connection


def tenant_upload_path(instance, filename: str, subdirectory: str = "") -> str:
    """
    Generate a tenant-scoped upload path for media files.

    Usage in models:
        from functools import partial
        from apps.core.storage import tenant_upload_path

        class Product(models.Model):
            image = models.ImageField(
                upload_to=partial(tenant_upload_path, subdirectory="products")
            )
    """
    schema_name = getattr(connection, "schema_name", "public")
    if subdirectory:
        return f"{schema_name}/{subdirectory}/{filename}"
    return f"{schema_name}/{filename}"


def make_tenant_upload_to(subdirectory: str):
    """
    Factory function for creating upload_to callables with a fixed subdirectory.

    Usage:
        class Product(models.Model):
            image = models.ImageField(upload_to=make_tenant_upload_to("products"))
    """
    def upload_path(instance, filename: str) -> str:
        schema_name = getattr(connection, "schema_name", "public")
        return f"{schema_name}/{subdirectory}/{filename}"
    return upload_path
