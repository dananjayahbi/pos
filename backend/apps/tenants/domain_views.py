"""Domain management views for tenants."""

import logging

from django.conf import settings
from django.db import connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tenants.models import Domain, Tenant

logger = logging.getLogger(__name__)


class TenantDomainListView(APIView):
    """
    GET  /api/v1/tenant/domains/    — list current tenant's domains
    POST /api/v1/tenant/domains/    — add a custom domain
    Access: authenticated tenant user (admin role or higher)
    """

    permission_classes = [IsAuthenticated]

    def _get_current_tenant(self):
        """Get the Tenant for the current request schema."""
        schema_name = connection.schema_name
        try:
            return Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            return None

    def get(self, request):
        tenant = self._get_current_tenant()
        if not tenant:
            return Response({"error": "Tenant not found."}, status=404)

        domains = Domain.objects.filter(tenant=tenant).values(
            "id", "domain", "is_primary", "domain_type", "is_verified", "ssl_status"
        )
        return Response(list(domains))

    def post(self, request):
        tenant = self._get_current_tenant()
        if not tenant:
            return Response({"error": "Tenant not found."}, status=404)

        domain_name = request.data.get("domain", "").lower().strip()
        if not domain_name:
            return Response({"error": "Domain name is required."}, status=400)

        # Basic validation
        if len(domain_name) < 4 or "." not in domain_name:
            return Response({"error": "Invalid domain name."}, status=400)

        # Don't allow platform subdomains
        base_domain = getattr(settings, "TENANT_BASE_DOMAIN", "localhost")
        if domain_name.endswith(f".{base_domain}"):
            return Response(
                {"error": f"Cannot use *.{base_domain} domains as custom domains."},
                status=400,
            )

        # Check if domain is already in use
        if Domain.objects.filter(domain=domain_name).exists():
            return Response(
                {"error": "This domain is already registered."},
                status=400,
            )

        domain = Domain.objects.create(
            domain=domain_name,
            tenant=tenant,
            is_primary=False,
            domain_type="custom",
            is_verified=False,
            ssl_status="none",
        )

        logger.info("Custom domain added: %s for tenant %s", domain_name, tenant.schema_name)

        return Response(
            {
                "id": domain.id,
                "domain": domain.domain,
                "is_primary": domain.is_primary,
                "domain_type": domain.domain_type,
                "is_verified": domain.is_verified,
                "ssl_status": domain.ssl_status,
                "verification_instructions": {
                    "type": "CNAME",
                    "name": "_lcc-verify",
                    "value": f"{tenant.slug}.{base_domain}",
                    "description": (
                        f"Add a CNAME record: _lcc-verify.{domain_name} → {tenant.slug}.{base_domain}"
                    ),
                },
            },
            status=201,
        )


class TenantDomainDeleteView(APIView):
    """
    DELETE /api/v1/tenant/domains/{domain_id}/
    Remove a custom domain (cannot delete primary platform domain).
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, domain_id):
        schema_name = connection.schema_name
        try:
            tenant = Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found."}, status=404)

        try:
            domain = Domain.objects.get(id=domain_id, tenant=tenant)
        except Domain.DoesNotExist:
            return Response({"error": "Domain not found."}, status=404)

        if domain.is_primary:
            return Response(
                {"error": "Cannot delete the primary domain."},
                status=400,
            )

        domain.delete()
        return Response(status=204)


class TenantDomainVerifyView(APIView):
    """
    POST /api/v1/tenant/domains/{domain_id}/verify/
    Attempt DNS verification for a custom domain.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, domain_id):
        schema_name = connection.schema_name
        try:
            tenant = Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found."}, status=404)

        try:
            domain = Domain.objects.get(id=domain_id, tenant=tenant)
        except Domain.DoesNotExist:
            return Response({"error": "Domain not found."}, status=404)

        if domain.is_verified:
            return Response({"verified": True, "message": "Domain is already verified."})

        base_domain = getattr(settings, "TENANT_BASE_DOMAIN", "localhost")
        expected_cname = f"{tenant.slug}.{base_domain}"
        check_record = f"_lcc-verify.{domain.domain}"

        try:
            import dns.resolver  # dnspython — optional dependency
            answers = dns.resolver.resolve(check_record, "CNAME")
            for rdata in answers:
                cname_value = str(rdata.target).rstrip(".")
                if cname_value == expected_cname:
                    domain.is_verified = True
                    domain.save(update_fields=["is_verified"])
                    logger.info(
                        "Domain verified: %s for tenant %s",
                        domain.domain,
                        tenant.schema_name,
                    )
                    return Response({
                        "verified": True,
                        "message": "Domain successfully verified!",
                    })

            return Response({
                "verified": False,
                "message": (
                    f"CNAME record found but value does not match. "
                    f"Expected: {expected_cname}"
                ),
            })

        except ImportError:
            return Response({
                "verified": False,
                "message": "DNS verification is not available. Install dnspython.",
            }, status=503)
        except Exception as exc:  # dns.resolver.NXDOMAIN, NoAnswer, DNSException
            exc_type = type(exc).__name__
            if "NXDOMAIN" in exc_type:
                return Response({
                    "verified": False,
                    "message": (
                        f"DNS record not found. Add a CNAME record: "
                        f"{check_record} → {expected_cname}"
                    ),
                })
            if "NoAnswer" in exc_type:
                return Response({
                    "verified": False,
                    "message": f"No CNAME record found at {check_record}.",
                })
            logger.warning("DNS verification error for %s: %s", domain.domain, exc)
            return Response({
                "verified": False,
                "message": "DNS lookup failed. Please try again later.",
            })
