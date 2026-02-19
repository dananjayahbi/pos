"""
LankaCommerce Cloud - Tenant Signals.

Provides automatic creation of related records when tenants are
created. Ensures every new tenant has a TenantSettings record
with sensible defaults.

Signal:
    create_tenant_settings — post_save on Tenant model.
    Creates a TenantSettings record when a new Tenant is saved
    for the first time (created=True). Uses get_or_create to
    prevent duplicates if called multiple times.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="tenants.Tenant")
def create_tenant_settings(sender, instance, created, **kwargs):
    """
    Auto-create TenantSettings when a new Tenant is created.

    This signal fires on every Tenant.save(), but only creates
    a TenantSettings record when the tenant is first created
    (created=True). Uses get_or_create as a safety measure
    against duplicate signal firing.

    Args:
        sender: The Tenant model class.
        instance: The Tenant instance that was saved.
        created: True if this is a new record, False if update.
        **kwargs: Additional signal arguments.
    """
    if created:
        from apps.tenants.models import TenantSettings

        _, settings_created = TenantSettings.objects.get_or_create(
            tenant=instance,
        )
        if settings_created:
            logger.info(
                "Created TenantSettings for tenant '%s' (schema: %s)",
                instance.name,
                instance.schema_name,
            )
