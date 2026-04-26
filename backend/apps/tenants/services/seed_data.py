"""
Seed default data for a newly provisioned tenant schema.
All code here runs inside schema_context(tenant.schema_name).
"""

import logging

logger = logging.getLogger(__name__)


def seed_tenant_defaults(tenant) -> None:
    """Seed all default data for a new tenant."""
    logger.info("Seeding defaults for tenant: %s", tenant.schema_name)
    _seed_currencies()
    _seed_tax_rates()
    _seed_product_categories()
    _seed_payment_methods()
    logger.info("Seeding complete for tenant: %s", tenant.schema_name)


def _seed_currencies() -> None:
    """Seed default currency (LKR)."""
    try:
        from apps.accounting.models import Currency  # noqa: PLC0415
        Currency.objects.get_or_create(
            code="LKR",
            defaults={"name": "Sri Lankan Rupee", "symbol": "Rs", "is_default": True},
        )
    except Exception as exc:
        logger.warning("Could not seed currencies: %s", exc)


def _seed_tax_rates() -> None:
    """Seed default tax rate (VAT 18%)."""
    try:
        from apps.accounting.models import TaxRate  # noqa: PLC0415
        TaxRate.objects.get_or_create(
            name="VAT 18%",
            defaults={"rate": 18.0, "is_default": True, "is_active": True},
        )
    except Exception as exc:
        logger.warning("Could not seed tax rates: %s", exc)


def _seed_product_categories() -> None:
    """Seed a default 'General' product category."""
    try:
        from apps.inventory.models import Category  # noqa: PLC0415
        Category.objects.get_or_create(
            name="General",
            defaults={"description": "General products", "is_active": True},
        )
    except Exception as exc:
        logger.warning("Could not seed product categories: %s", exc)


def _seed_payment_methods() -> None:
    """Seed default payment methods."""
    try:
        from apps.payments.models import PaymentMethod  # noqa: PLC0415
        for name, code in [("Cash", "cash"), ("Card", "card"), ("Bank Transfer", "bank_transfer")]:
            PaymentMethod.objects.get_or_create(
                code=code,
                defaults={"name": name, "is_active": True},
            )
    except Exception as exc:
        logger.warning("Could not seed payment methods: %s", exc)
