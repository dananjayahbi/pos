"""Inventory application configuration."""

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """Configuration for the Inventory application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.inventory"
    label = "inventory"
    verbose_name = "Inventory Management"
