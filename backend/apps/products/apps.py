"""Products application configuration."""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration for the Products application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    label = "products"
    verbose_name = "Product Management"
