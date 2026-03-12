"""
Products models package.

Exports all models from the products application for convenient
importing. Models can be imported directly from apps.products.models:

    from apps.products.models import (
        Brand, Category, Product, ProductImage, ProductVariant,
        TaxClass, UnitOfMeasure,
    )
"""

# Supporting models
from apps.products.models.brand import Brand
from apps.products.models.tax_class import TaxClass
from apps.products.models.unit_of_measure import UnitOfMeasure

# Core models
from apps.products.models.category import Category
from apps.products.models.image import ProductImage
from apps.products.models.product import Product
from apps.products.models.variant import ProductVariant

# Managers
from apps.products.models.managers import (
    CategoryManager,
    CategoryQuerySet,
    ProductManager,
    ProductQuerySet,
)

__all__ = [
    "Brand",
    "Category",
    "CategoryManager",
    "CategoryQuerySet",
    "Product",
    "ProductImage",
    "ProductManager",
    "ProductQuerySet",
    "ProductVariant",
    "TaxClass",
    "UnitOfMeasure",
]
