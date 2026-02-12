"""
Core application configuration.

Provides base models, mixins, utilities, and shared functionality
for the LankaCommerce Cloud platform.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the Core application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = "Core Framework"
