"""Tenant registration and management views."""

import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tenants.serializers import (
    SlugAvailabilitySerializer,
    TenantRegistrationSerializer,
)
from apps.tenants.services.provisioning import provision_tenant

logger = logging.getLogger(__name__)


class TenantSlugAvailabilityView(APIView):
    """
    GET /api/v1/tenants/check-slug/?slug={slug}
    Returns whether a slug is available for registration.
    Public endpoint — no authentication required.
    """

    permission_classes = [AllowAny]
    throttle_scope = "slug_check"

    def get(self, request):
        serializer = SlugAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        slug = serializer.validated_data["slug"]

        from apps.tenants.models import Tenant
        is_available = not Tenant.objects.filter(slug=slug).exists()

        return Response({
            "slug": slug,
            "available": is_available,
            "subdomain": f"{slug}.{settings.TENANT_BASE_DOMAIN}",
        })


class TenantRegistrationView(APIView):
    """
    POST /api/v1/tenants/register/
    Registers a new business tenant, provisions its schema, and returns
    the subdomain URL + trial info.
    Public endpoint — no authentication required.
    """

    permission_classes = [AllowAny]
    throttle_scope = "registration"

    def post(self, request):
        serializer = TenantRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = provision_tenant(
                slug=data["slug"],
                business_name=data["business_name"],
                business_type=data["business_type"],
                industry=data["industry"],
                contact_name=data["contact_name"],
                contact_email=data["email"],
                contact_phone=data.get("contact_phone", ""),
                password=data["password"],
                city=data.get("city", ""),
                province=data.get("province", ""),
                plan_id=data.get("plan_id"),
            )
        except Exception as exc:
            logger.exception("Tenant provisioning failed for slug=%s", data.get("slug"))
            return Response(
                {"error": "provisioning_failed", "detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(result, status=status.HTTP_201_CREATED)
