"""
POSPayment model — records every payment attempt against a POS cart.

Supports cash, card, mobile, bank transfer, store credit, and PayHere
with split-payment capability (multiple payments per cart).
"""

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.pos.constants import (
    PAYMENT_METHOD_CASH,
    PAYMENT_METHOD_CHOICES,
    PAYMENT_STATUS_CHOICES,
    PAYMENT_STATUS_PENDING,
)

AMOUNT_MAX_DIGITS = 12
AMOUNT_DECIMAL_PLACES = 2


class POSPayment(BaseModel):
    """
    Payment record for POS transactions.

    Supports multiple payment methods and split payments.
    Sum of all COMPLETED payments must equal or exceed the cart grand_total.
    """

    # ── Relationships ───────────────────────────────────────────────

    cart = models.ForeignKey(
        "pos.POSCart",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Cart"),
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pos_payments_processed",
        verbose_name=_("Processed By"),
    )

    # ── Payment Core ────────────────────────────────────────────────

    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name=_("Payment Method"),
    )
    amount = models.DecimalField(
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        verbose_name=_("Amount (LKR)"),
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING,
        verbose_name=_("Status"),
    )

    # ── Cash-specific ───────────────────────────────────────────────

    amount_tendered = models.DecimalField(
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name=_("Amount Tendered"),
        help_text=_("Cash given by customer"),
    )
    change_due = models.DecimalField(
        max_digits=AMOUNT_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name=_("Change Due"),
        help_text=_("Change to return to customer"),
    )

    # ── Gateway / reference ─────────────────────────────────────────

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name=_("Reference Number"),
        help_text=_("External payment reference (bank/mobile)"),
    )
    authorization_code = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name=_("Authorization Code"),
        help_text=_("Card payment authorization code"),
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
        verbose_name=_("Transaction ID"),
        help_text=_("Gateway transaction identifier"),
    )
    gateway_response = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Gateway Response"),
        help_text=_("Full JSON response from payment gateway"),
    )

    # ── Timestamps ──────────────────────────────────────────────────

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Paid At"),
    )
    voided_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Voided At"),
    )

    # ── Notes ───────────────────────────────────────────────────────

    notes = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Notes"),
    )

    class Meta:
        db_table = "pos_payment"
        ordering = ["-created_on"]
        verbose_name = _("POS Payment")
        verbose_name_plural = _("POS Payments")
        indexes = [
            models.Index(fields=["cart", "status"], name="pos_pay_cart_status"),
            models.Index(fields=["method"], name="pos_pay_method"),
            models.Index(fields=["-created_on"], name="pos_pay_created"),
            models.Index(fields=["reference_number"], name="pos_pay_ref"),
        ]

    def __str__(self):
        return f"Payment {self.method} - LKR {self.amount} ({self.status})"

    # ── helpers ─────────────────────────────────────────────────────

    @property
    def is_exact_change(self):
        if self.method != PAYMENT_METHOD_CASH:
            return None
        if self.amount_tendered is None:
            return None
        return self.amount_tendered == self.amount

    def calculate_change(self):
        """Calculate and return change due (does not save)."""
        if self.amount_tendered is None or self.amount is None:
            return Decimal("0.00")
        return max(self.amount_tendered - self.amount, Decimal("0.00"))
