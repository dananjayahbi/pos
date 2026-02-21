"""
ProductVariant model for the products application.

Defines the ProductVariant model which supports product variations
such as size, color, material, or weight. Each variant can have
its own SKU, barcode, and pricing independent of the parent product.
"""

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.mixins import UUIDMixin, TimestampMixin
from apps.products.constants import (
    VARIANT_ATTRIBUTE_CHOICES,
    VARIANT_ATTR_SIZE,
)


# Reuse pricing constants from product module
PRICE_MAX_DIGITS = 10
PRICE_DECIMAL_PLACES = 2


class ProductVariant(UUIDMixin, TimestampMixin, models.Model):
    """
    Product variant model for size, color, and other variations.

    Each variant represents a specific variation of a product
    (e.g., "Red - Large", "Blue - Small"). Variants can have their
    own SKU, barcode, and pricing that overrides the parent product.

    Fields:
        product: FK to the parent Product.
        attribute_type: Type of variation (size, color, etc.).
        attribute_value: The specific value (e.g., "XL", "Red").
        sku: Variant-specific SKU, unique per tenant.
        barcode: Variant-specific barcode.
        price_override: Optional price override for this variant.
        cost_override: Optional cost override for this variant.
        is_active: Whether this variant is available.
        sort_order: Controls display order.
    """

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Product",
        help_text="The parent product this variant belongs to.",
    )

    # ── Variant Attributes ──────────────────────────────────────────
    attribute_type = models.CharField(
        max_length=20,
        choices=VARIANT_ATTRIBUTE_CHOICES,
        default=VARIANT_ATTR_SIZE,
        verbose_name="Attribute Type",
        help_text="Type of variation (size, color, etc.).",
    )
    attribute_value = models.CharField(
        max_length=100,
        verbose_name="Attribute Value",
        help_text="Specific value (e.g., 'XL', 'Red', '500g').",
    )

    # ── Variant Identification ──────────────────────────────────────
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Variant SKU",
        help_text="Variant-specific SKU. Unique per tenant.",
    )
    barcode = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Variant Barcode",
        help_text="Variant-specific barcode.",
    )

    # ── Variant Pricing (LKR) ──────────────────────────────────────
    price_override = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Price Override (₨)",
        help_text="Override selling price for this variant. Null uses product price.",
    )
    cost_override = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Cost Override (₨)",
        help_text="Override cost price for this variant. Null uses product cost.",
    )

    # ── Visibility ──────────────────────────────────────────────────
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active",
        help_text="Whether this variant is currently available.",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sort Order",
        help_text="Controls display order. Lower values appear first.",
    )

    class Meta:
        app_label = "products"
        db_table = "products_productvariant"
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ["sort_order", "attribute_type"]
        indexes = [
            models.Index(
                fields=["product", "attribute_type"],
                name="idx_variant_product_attr",
            ),
            models.Index(
                fields=["sku"],
                name="idx_variant_sku",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "attribute_type", "attribute_value"],
                name="uq_variant_product_attr_value",
            ),
        ]

    def __str__(self):
        """Return variant description."""
        return f"{self.product_id} - {self.attribute_type}: {self.attribute_value}"

    @property
    def effective_price(self):
        """Return variant price or fall back to product selling price."""
        if self.price_override is not None:
            return self.price_override
        return self.product.selling_price

    @property
    def effective_cost(self):
        """Return variant cost or fall back to product cost price."""
        if self.cost_override is not None:
            return self.cost_override
        return self.product.cost_price
