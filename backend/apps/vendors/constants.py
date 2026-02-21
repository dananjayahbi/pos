"""
Vendors constants module.

Defines choices, status values, and other constants used across
the vendors application models. In the document series this app
is referred to as "suppliers" — the vendors app serves the same
purpose under the project's naming convention.
"""

# ════════════════════════════════════════════════════════════════════════
# Payment Terms Choices
# ════════════════════════════════════════════════════════════════════════

PAYMENT_TERM_IMMEDIATE = "immediate"
PAYMENT_TERM_NET_15 = "net_15"
PAYMENT_TERM_NET_30 = "net_30"
PAYMENT_TERM_NET_60 = "net_60"
PAYMENT_TERM_COD = "cod"

PAYMENT_TERMS_CHOICES = [
    (PAYMENT_TERM_IMMEDIATE, "Immediate"),
    (PAYMENT_TERM_NET_15, "Net 15 Days"),
    (PAYMENT_TERM_NET_30, "Net 30 Days"),
    (PAYMENT_TERM_NET_60, "Net 60 Days"),
    (PAYMENT_TERM_COD, "Cash on Delivery"),
]

# Default payment terms for new suppliers
DEFAULT_PAYMENT_TERMS = PAYMENT_TERM_NET_30
