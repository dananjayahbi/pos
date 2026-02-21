"""
Vendors models package.

Exports all models from the vendors application for convenient
importing. Models can be imported directly from apps.vendors.models:

    from apps.vendors.models import Supplier
"""

from apps.vendors.models.supplier import Supplier

__all__ = [
    "Supplier",
]
