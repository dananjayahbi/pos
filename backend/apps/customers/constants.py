"""
Customers constants module.

Defines choices, status values, and other constants used across
the customers application models.
"""

# ════════════════════════════════════════════════════════════════════════
# Customer Type Choices
# ════════════════════════════════════════════════════════════════════════

CUSTOMER_TYPE_INDIVIDUAL = "individual"
CUSTOMER_TYPE_BUSINESS = "business"
CUSTOMER_TYPE_WHOLESALE = "wholesale"
CUSTOMER_TYPE_VIP = "vip"

CUSTOMER_TYPE_CHOICES = [
    (CUSTOMER_TYPE_INDIVIDUAL, "Individual"),
    (CUSTOMER_TYPE_BUSINESS, "Business / Corporate"),
    (CUSTOMER_TYPE_WHOLESALE, "Wholesale Buyer"),
    (CUSTOMER_TYPE_VIP, "VIP Customer"),
]

# Default customer type for new customers
DEFAULT_CUSTOMER_TYPE = CUSTOMER_TYPE_INDIVIDUAL

# Default credit limit (in LKR)
DEFAULT_CREDIT_LIMIT = 0
