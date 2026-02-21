"""
Orders constants module.

Defines choices, status values, and other constants used across
the orders application models.
"""

# ════════════════════════════════════════════════════════════════════════
# Order Status Choices
# ════════════════════════════════════════════════════════════════════════

ORDER_STATUS_PENDING = "pending"
ORDER_STATUS_CONFIRMED = "confirmed"
ORDER_STATUS_PROCESSING = "processing"
ORDER_STATUS_SHIPPED = "shipped"
ORDER_STATUS_DELIVERED = "delivered"
ORDER_STATUS_CANCELLED = "cancelled"
ORDER_STATUS_RETURNED = "returned"

ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING, "Pending"),
    (ORDER_STATUS_CONFIRMED, "Confirmed"),
    (ORDER_STATUS_PROCESSING, "Processing"),
    (ORDER_STATUS_SHIPPED, "Shipped"),
    (ORDER_STATUS_DELIVERED, "Delivered"),
    (ORDER_STATUS_CANCELLED, "Cancelled"),
    (ORDER_STATUS_RETURNED, "Returned"),
]

# Default order status for new orders
DEFAULT_ORDER_STATUS = ORDER_STATUS_PENDING
