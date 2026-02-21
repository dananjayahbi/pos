"""
Product model for the products application.

Defines the core Product model which represents items in the
tenant's product catalog. Each product belongs to a category
and includes pricing, identification (SKU, barcode), and
descriptive fields. Products are tenant-specific — each tenant
has its own independent product catalog.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from apps.core.mixins import UUIDMixin, TimestampMixin
from apps.products.constants import (
    PRODUCT_STATUS_CHOICES,
    PRODUCT_STATUS_DRAFT,
    TAX_TYPE_CHOICES,
    TAX_TYPE_STANDARD,
)


# ════════════════════════════════════════════════════════════════════════
# Pricing Constants
# ════════════════════════════════════════════════════════════════════════

# LKR currency: max 10 digits, 2 decimal places
PRICE_MAX_DIGITS = 10
PRICE_DECIMAL_PLACES = 2


class Product(UUIDMixin, TimestampMixin, models.Model):
    """
    Core product model for the tenant catalog.

    Represents a single product item with identification (SKU, barcode),
    categorization, pricing (cost, selling, MRP, wholesale), and status.
    All pricing fields use LKR (Sri Lankan Rupee) with PRICE_MAX_DIGITS=10
    and PRICE_DECIMAL_PLACES=2.

    Fields:
        name: Product display name (max 255 chars).
        slug: URL-friendly identifier, unique per tenant schema.
        description: Optional detailed product description.
        sku: Stock Keeping Unit, unique per tenant schema.
        barcode: Optional barcode (EAN-13, UPC-A, or custom format).
        category: FK to Category model for product categorization.
        cost_price: Purchase cost from supplier (LKR).
        selling_price: Standard selling price (LKR).
        mrp: Maximum Retail Price — common in Sri Lankan retail (LKR).
        wholesale_price: Bulk/wholesale purchase price (LKR).
        status: Product lifecycle status (draft, active, inactive, discontinued).
    """

    # ── Identification Fields ───────────────────────────────────────
    name = models.CharField(
        max_length=255,
        verbose_name="Product Name",
        help_text="Display name of the product.",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug",
        help_text="URL-friendly identifier. Unique per tenant.",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Description",
        help_text="Detailed product description.",
    )

    # ── SKU & Barcode ───────────────────────────────────────────────
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU",
        help_text="Stock Keeping Unit. Unique per tenant.",
    )
    barcode = models.CharField(
        max_length=50,
        blank=True,
        default="",
        db_index=True,
        verbose_name="Barcode",
        help_text="Product barcode (EAN-13, UPC-A, or custom format).",
    )

    # ── Category Relationship ───────────────────────────────────────
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Category",
        help_text="Product category. Products remain if category is deleted.",
    )

    # ── Pricing Fields (LKR) ───────────────────────────────────────
    cost_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Cost Price (₨)",
        help_text="Purchase cost from supplier in LKR.",
    )
    selling_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Selling Price (₨)",
        help_text="Standard selling price in LKR.",
    )
    mrp = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="MRP (₨)",
        help_text="Maximum Retail Price in LKR. Common in Sri Lankan retail.",
    )
    wholesale_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Wholesale Price (₨)",
        help_text="Bulk/wholesale purchase price in LKR.",
    )

    # ── Tax Fields (Sri Lankan VAT) ────────────────────────────────
    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPE_CHOICES,
        default=TAX_TYPE_STANDARD,
        verbose_name="Tax Type",
        help_text="Tax classification for Sri Lankan VAT.",
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18,
        validators=[MinValueValidator(0)],
        verbose_name="Tax Rate (%)",
        help_text="Tax rate percentage. Default: 18% (Sri Lankan standard VAT).",
    )
    is_tax_inclusive = models.BooleanField(
        default=False,
        verbose_name="Tax Inclusive",
        help_text="Whether the selling price includes tax.",
    )

    # ── Status ──────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=PRODUCT_STATUS_CHOICES,
        default=PRODUCT_STATUS_DRAFT,
        db_index=True,
        verbose_name="Status",
        help_text="Product lifecycle status.",
    )

    class Meta:
        app_label = "products"
        db_table = "products_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_on"]
        indexes = [
            models.Index(
                fields=["status", "created_on"],
                name="idx_product_status_created",
            ),
            models.Index(
                fields=["category", "status"],
                name="idx_product_category_status",
            ),
            models.Index(
                fields=["sku"],
                name="idx_product_sku",
            ),
        ]

    def __str__(self):
        """Return product name with SKU."""
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.selling_price and self.cost_price and self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0

    @property
    def is_active(self):
        """Return True if product status is active."""
        from apps.products.constants import PRODUCT_STATUS_ACTIVE
        return self.status == PRODUCT_STATUS_ACTIVE
