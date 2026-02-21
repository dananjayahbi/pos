"""
Orders models package.

Exports all models from the orders application for convenient
importing. Models can be imported directly from apps.orders.models:

    from apps.orders.models import Order, OrderItem
"""

from apps.orders.models.order import Order
from apps.orders.models.order_item import OrderItem

__all__ = [
    "Order",
    "OrderItem",
]
