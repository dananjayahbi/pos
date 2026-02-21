"""
OrderItem model for the orders application.

Defines the OrderItem model which stores individual line items
within a customer order. Each line item links to a product,
records the ordered quantity, and captures pricing in LKR (₨).
"""

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.mixins import UUIDMixin, TimestampMixin

# Price field constants (consistent with products and order apps)
PRICE_MAX_DIGITS = 10
PRICE_DECIMAL_PLACES = 2

# Quantity field constants
QUANTITY_MAX_DIGITS = 12
QUANTITY_DECIMAL_PLACES = 3


class OrderItem(UUIDMixin, TimestampMixin, models.Model):
    """
    Line item within a customer order.

    Each OrderItem represents a single product entry in an order,
    capturing the product reference, ordered quantity, unit price
    at the time of order, and the calculated line total. All monetary
    values are stored in LKR (₨).

    Fields:
        order: FK to the parent Order.
        product: FK to the Product being ordered.
        quantity: Number of units ordered (must be > 0).
        unit_price: Price per unit at the time of order (LKR).
        discount_amount: Discount applied to this line item (LKR).
        tax_amount: Tax amount for this line item (LKR).
        line_total: Total amount for this line item (LKR).
        notes: Optional notes about this line item.
    """

    # ── Order FK ────────────────────────────────────────────────────
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Order",
        help_text="The parent order this item belongs to.",
    )

    # ── Product FK ──────────────────────────────────────────────────
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Product",
        help_text="The product being ordered.",
    )

    # ── Quantity ────────────────────────────────────────────────────
    quantity = models.DecimalField(
        max_digits=QUANTITY_MAX_DIGITS,
        decimal_places=QUANTITY_DECIMAL_PLACES,
        default=1,
        validators=[MinValueValidator(0.001)],
        verbose_name="Quantity",
        help_text="Number of units ordered. Must be greater than zero.",
    )

    # ── Pricing (LKR) ──────────────────────────────────────────────
    unit_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Unit Price (LKR)",
        help_text="Price per unit at the time of order, in LKR (₨).",
    )
    discount_amount = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Discount (LKR)",
        help_text="Discount applied to this line item, in LKR (₨).",
    )
    tax_amount = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tax Amount (LKR)",
        help_text="Tax amount for this line item, in LKR (₨).",
    )
    line_total = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        verbose_name="Line Total (LKR)",
        help_text="Total amount for this line item, in LKR (₨).",
    )

    # ── Notes ───────────────────────────────────────────────────────
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notes",
        help_text="Optional notes about this line item.",
    )

    class Meta:
        db_table = "orders_orderitem"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["created_on"]
        indexes = [
            models.Index(
                fields=["order", "product"],
                name="idx_orderitem_order_product",
            ),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product} on {self.order}"

    def calculate_line_total(self):
        """Calculate the line total from quantity, unit price, tax, and discount."""
        self.line_total = (
            (self.quantity * self.unit_price)
            + self.tax_amount
            - self.discount_amount
        )

    @property
    def subtotal(self):
        """Return quantity × unit_price before tax and discount."""
        return self.quantity * self.unit_price
