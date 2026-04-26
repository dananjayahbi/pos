"""Tenant registration serializers."""

import re
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from apps.tenants.models import Domain, Tenant


RESERVED_SLUGS = {
    "www", "api", "admin", "mail", "smtp", "ftp", "static", "media",
    "platform", "app", "dashboard", "login", "register", "billing",
    "support", "help", "docs", "status", "staging", "dev", "test",
    "demo", "sandbox", "public", "shared", "tenant",
}

SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9\-]{1,30}[a-z0-9]$")


class TenantRegistrationSerializer(serializers.Serializer):
    """Serializer for new tenant (business) registration."""

    # Account
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    contact_name = serializers.CharField(max_length=150)

    # Subdomain
    slug = serializers.CharField(max_length=32)

    # Business
    business_name = serializers.CharField(max_length=200)
    business_type = serializers.ChoiceField(choices=[
        ("sole_proprietor", "Sole Proprietor"),
        ("partnership", "Partnership"),
        ("pvt_ltd", "Private Limited"),
        ("plc", "Public Limited Company"),
        ("ngo", "NGO / Non-Profit"),
        ("other", "Other"),
    ])
    industry = serializers.ChoiceField(choices=[
        ("retail", "Retail"),
        ("wholesale", "Wholesale"),
        ("manufacturing", "Manufacturing"),
        ("food_beverage", "Food & Beverage"),
        ("fashion_apparel", "Fashion & Apparel"),
        ("electronics", "Electronics"),
        ("pharmacy", "Pharmacy"),
        ("services", "Services"),
        ("other", "Other"),
    ])
    contact_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    # Optional address
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    province = serializers.CharField(max_length=100, required=False, allow_blank=True)

    # Plan (optional — defaults to trial)
    plan_id = serializers.CharField(required=False, allow_null=True)

    def validate_slug(self, value):
        value = value.lower().strip()
        if value in RESERVED_SLUGS:
            raise serializers.ValidationError(
                f"'{value}' is a reserved name and cannot be used."
            )
        if not SLUG_PATTERN.match(value):
            raise serializers.ValidationError(
                "Slug must be 3-32 characters, lowercase letters, digits, and hyphens only. "
                "Cannot start or end with a hyphen."
            )
        if Tenant.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                f"'{value}' is already taken. Please choose a different subdomain."
            )
        return value

    def validate_email(self, value):
        value = value.lower().strip()
        # Check email not already registered as a tenant owner
        # (cross-tenant uniqueness via public schema — email stored on Tenant)
        if Tenant.objects.filter(contact_email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate(self, data):
        return data


class TenantRegistrationResponseSerializer(serializers.Serializer):
    """Shape of the successful registration response."""

    tenant_id = serializers.CharField()
    business_name = serializers.CharField()
    slug = serializers.CharField()
    subdomain_url = serializers.CharField()
    trial_ends_at = serializers.DateField()
    admin_email = serializers.EmailField()
    message = serializers.CharField()


class SlugAvailabilitySerializer(serializers.Serializer):
    """Check if a slug is available."""
    slug = serializers.CharField(max_length=32)

    def validate_slug(self, value):
        value = value.lower().strip()
        if value in RESERVED_SLUGS:
            raise serializers.ValidationError(f"'{value}' is reserved.")
        if not SLUG_PATTERN.match(value):
            raise serializers.ValidationError("Invalid slug format.")
        return value
