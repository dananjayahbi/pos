"""
Order model for the orders application.

Defines the Order model which tracks customer purchases within a
tenant schema. Each order has a unique order number, links to a
customer, progresses through a status workflow, and records
financial totals (subtotal, tax, discount, total) in LKR.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from apps.orders.constants import (
    DEFAULT_ORDER_STATUS,
    ORDER_STATUS_CHOICES,
)

# Price field constants (consistent with products app)
PRICE_MAX_DIGITS = 10
PRICE_DECIMAL_PLACES = 2


class Order(UUIDMixin, TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Customer purchase order.

    Tracks the full lifecycle of a customer order from creation to
    delivery or cancellation. Orders link to a customer and contain
    order items (defined in OrderItem model). Financial totals are
    stored in LKR (₨).

    Status workflow:
        pending → confirmed → processing → shipped → delivered
                                                    ↘ cancelled
                                                    ↘ returned

    Fields:
        order_number: Unique order identifier within the tenant.
            Uses tenant-specific prefix + sequence.
        customer: FK to Customer who placed the order.
        status: Current order status in the workflow.
        order_date: Date/time the order was placed (defaults to now).
        subtotal: Sum of all order item amounts before tax/discount.
        tax_amount: Total tax amount for the order.
        discount_amount: Total discount applied to the order.
        total_amount: Final amount payable (subtotal + tax - discount).
        notes: Optional notes about the order.
        created_by: User who created the order.
    """

    # ── Order Number ────────────────────────────────────────────────
    order_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name="Order Number",
        help_text=(
            "Unique order identifier within the tenant. "
            "Uses tenant-specific prefix + sequence."
        ),
    )

    # ── Customer FK ─────────────────────────────────────────────────
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Customer",
        help_text="The customer who placed this order.",
    )

    # ── Status ──────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default=DEFAULT_ORDER_STATUS,
        db_index=True,
        verbose_name="Order Status",
        help_text="Current status in the order workflow.",
    )

    # ── Order Date ──────────────────────────────────────────────────
    order_date = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name="Order Date",
        help_text="Date and time the order was placed (Asia/Colombo).",
    )

    # ── Financial Totals (LKR) ──────────────────────────────────────
    subtotal = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        verbose_name="Subtotal (LKR)",
        help_text="Sum of all order item amounts before tax and discount.",
    )
    tax_amount = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        verbose_name="Tax Amount (LKR)",
        help_text="Total tax amount for the order.",
    )
    discount_amount = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        verbose_name="Discount Amount (LKR)",
        help_text="Total discount applied to the order.",
    )
    total_amount = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        default=0,
        verbose_name="Total Amount (LKR)",
        help_text="Final amount payable (subtotal + tax - discount).",
    )

    # ── Notes & Audit ───────────────────────────────────────────────
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notes",
        help_text="Optional notes about this order.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_orders",
        verbose_name="Created By",
        help_text="The user who created this order.",
    )

    class Meta:
        db_table = "orders_order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-order_date"]
        indexes = [
            models.Index(
                fields=["status", "order_date"],
                name="idx_order_status_date",
            ),
            models.Index(
                fields=["customer", "status"],
                name="idx_order_customer_status",
            ),
            models.Index(
                fields=["-order_date"],
                name="idx_order_date_desc",
            ),
        ]

    def __str__(self):
        return f"Order {self.order_number} — {self.get_status_display()}"

    def calculate_totals(self):
        """Recalculate order totals from order items."""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount

    @property
    def is_editable(self):
        """Return True if the order can still be modified."""
        return self.status in ("pending", "confirmed")

    @property
    def is_completed(self):
        """Return True if the order has been delivered."""
        return self.status == "delivered"

    @property
    def is_cancelled(self):
        """Return True if the order has been cancelled or returned."""
        return self.status in ("cancelled", "returned")
