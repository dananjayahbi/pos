"""
Customer model for the customers application.

Defines the Customer model which stores customer profiles for each
tenant. Customers can be individuals, businesses, wholesale buyers,
or VIP customers. Each customer type may have different credit
limits, pricing tiers, and contact patterns.
"""

from django.db import models

from apps.core.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from apps.customers.constants import (
    CUSTOMER_TYPE_CHOICES,
    DEFAULT_CUSTOMER_TYPE,
    DEFAULT_CREDIT_LIMIT,
)


class Customer(UUIDMixin, TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Customer record for a tenant.

    Supports individual walk-in customers as well as business and
    wholesale accounts. Each customer has name, contact, and address
    information plus a credit limit for trade accounts.

    Fields:
        first_name: Customer's first name (individuals).
        last_name: Customer's last name (individuals).
        business_name: Company / business name (business/wholesale).
        customer_type: Type classification (individual, business,
            wholesale, vip).
        email: Primary email address.
        phone: Primary phone number (+94 XX XXX XXXX format).
        mobile: Mobile phone number.
        billing_address_*: Billing address fields.
        shipping_address_*: Shipping address fields.
        credit_limit: Maximum credit allowed (in LKR). Default 0
            means no credit.
        current_balance: Outstanding balance owed by the customer.
        tax_id: Business registration / tax identification number.
        notes: Internal notes about the customer.
        is_active: Whether the customer is active.
    """

    # ── Name Fields ─────────────────────────────────────────────────
    first_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="First Name",
        help_text="Customer's first name (for individuals).",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Last Name",
        help_text="Customer's last name (for individuals).",
    )
    business_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Business Name",
        help_text="Company or business name (for business/wholesale customers).",
    )

    # ── Contact Fields ──────────────────────────────────────────────
    email = models.EmailField(
        blank=True,
        default="",
        verbose_name="Email",
        help_text="Primary email address for the customer.",
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        default="",
        verbose_name="Phone",
        help_text="Primary phone number (+94 XX XXX XXXX format).",
    )
    mobile = models.CharField(
        max_length=30,
        blank=True,
        default="",
        verbose_name="Mobile",
        help_text="Mobile phone number.",
    )

    # ── Billing Address ─────────────────────────────────────────────
    billing_address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Billing Address Line 1",
        help_text="Primary billing address line.",
    )
    billing_address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Billing Address Line 2",
        help_text="Secondary billing address line.",
    )
    billing_city = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Billing City",
    )
    billing_state_province = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Billing State / Province",
    )
    billing_postal_code = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Billing Postal Code",
    )
    billing_country = models.CharField(
        max_length=100,
        default="Sri Lanka",
        verbose_name="Billing Country",
    )

    # ── Shipping Address ────────────────────────────────────────────
    shipping_address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Shipping Address Line 1",
        help_text="Primary shipping address line.",
    )
    shipping_address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Shipping Address Line 2",
        help_text="Secondary shipping address line.",
    )
    shipping_city = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Shipping City",
    )
    shipping_state_province = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Shipping State / Province",
    )
    shipping_postal_code = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Shipping Postal Code",
    )
    shipping_country = models.CharField(
        max_length=100,
        default="Sri Lanka",
        verbose_name="Shipping Country",
    )

    # ── Type & Status ───────────────────────────────────────────────
    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default=DEFAULT_CUSTOMER_TYPE,
        db_index=True,
        verbose_name="Customer Type",
        help_text="Classification: individual, business, wholesale, or VIP.",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active",
        help_text="Whether this customer is active for transactions.",
    )

    # ── Financial Fields ────────────────────────────────────────────
    credit_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=DEFAULT_CREDIT_LIMIT,
        verbose_name="Credit Limit (LKR)",
        help_text="Maximum credit allowed in LKR (₨). 0 = no credit.",
    )
    current_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Current Balance (LKR)",
        help_text="Outstanding balance owed by the customer in LKR (₨).",
    )

    # ── Additional Fields ───────────────────────────────────────────
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Tax ID / BRN",
        help_text="Business registration number or tax identification.",
    )
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notes",
        help_text="Internal notes about this customer.",
    )

    class Meta:
        db_table = "customers_customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["first_name", "last_name", "business_name"]
        indexes = [
            models.Index(
                fields=["customer_type", "is_active"],
                name="idx_customer_type_active",
            ),
            models.Index(
                fields=["email"],
                name="idx_customer_email",
            ),
            models.Index(
                fields=["phone"],
                name="idx_customer_phone",
            ),
        ]

    def __str__(self):
        if self.business_name:
            return self.business_name
        full = f"{self.first_name} {self.last_name}".strip()
        return full or f"Customer {self.pk}"

    @property
    def full_name(self):
        """Return the customer's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        """Return business name for businesses, full name for individuals."""
        if self.business_name:
            return self.business_name
        return self.full_name or f"Customer {self.pk}"

    @property
    def has_credit(self):
        """Return True if this customer has a credit limit > 0."""
        return self.credit_limit > 0

    @property
    def available_credit(self):
        """Return remaining available credit (credit_limit - current_balance)."""
        if self.credit_limit <= 0:
            return 0
        return max(0, self.credit_limit - self.current_balance)
