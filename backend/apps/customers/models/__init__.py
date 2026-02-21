"""
Customers models package.

Exports all models from the customers application for convenient
importing. Models can be imported directly from apps.customers.models:

    from apps.customers.models import Customer
"""

from apps.customers.models.customer import Customer

__all__ = [
    "Customer",
]
