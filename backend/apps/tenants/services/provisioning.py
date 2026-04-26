"""
Real tenant provisioning service.
Replaces the stub provisioning_utils.py.
"""

import logging
import subprocess
import sys
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django_tenants.utils import schema_context

from apps.tenants.models import Domain, Tenant
from apps.tenants.services.seed_data import seed_tenant_defaults

logger = logging.getLogger(__name__)

TRIAL_DAYS = 7


def provision_tenant(
    *,
    slug: str,
    business_name: str,
    business_type: str,
    industry: str,
    contact_name: str,
    contact_email: str,
    contact_phone: str = "",
    password: str,
    city: str = "",
    province: str = "",
    plan_id: str | None = None,
) -> dict:
    """
    Provision a new tenant end-to-end:
    1. Create Tenant record (auto-creates PostgreSQL schema)
    2. Run migrate_schemas for the new schema
    3. Seed default data
    4. Create initial admin user
    5. Create Domain record
    6. Return provisioning result

    Raises on any failure — caller handles the exception.
    """

    trial_ends = timezone.now().date() + timedelta(days=TRIAL_DAYS)
    base_domain = settings.TENANT_BASE_DOMAIN

    # Step 1: Create Tenant (triggers auto_create_schema = True)
    logger.info("Creating tenant: slug=%s", slug)
    tenant = Tenant(
        name=business_name,
        slug=slug,
        business_type=business_type,
        industry=industry,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        city=city,
        province=province,
        on_trial=True,
        paid_until=trial_ends,
        status="active",
        onboarding_step=1,
    )
    tenant.save()  # ← this auto-creates the PostgreSQL schema
    logger.info("Schema created: %s", tenant.schema_name)

    # Step 2: Run migrations for the new schema
    _run_schema_migrations(tenant.schema_name)

    # Step 3: Seed default data inside the tenant schema
    with schema_context(tenant.schema_name):
        seed_tenant_defaults(tenant)

    # Step 4: Create initial admin user inside the tenant schema
    with schema_context(tenant.schema_name):
        admin_user = _create_tenant_admin(
            email=contact_email,
            password=password,
            full_name=contact_name,
        )

    # Step 5: Create Domain record
    subdomain = f"{slug}.{base_domain}"
    Domain.objects.create(
        domain=subdomain,
        tenant=tenant,
        is_primary=True,
        domain_type="platform",
        is_verified=True,
    )
    logger.info("Domain created: %s", subdomain)

    return {
        "tenant_id": str(tenant.id) if hasattr(tenant, "id") else tenant.schema_name,
        "business_name": tenant.name,
        "slug": tenant.slug,
        "subdomain_url": f"http://{subdomain}",
        "trial_ends_at": trial_ends.isoformat(),
        "admin_email": contact_email,
        "message": (
            f"Registration successful! Your store is ready at http://{subdomain}. "
            f"Your trial expires on {trial_ends.strftime('%B %d, %Y')}."
        ),
    }


def _run_schema_migrations(schema_name: str) -> None:
    """Run Django migrations for a specific tenant schema."""
    logger.info("Running migrations for schema: %s", schema_name)
    result = subprocess.run(
        [
            sys.executable,
            "manage.py",
            "migrate_schemas",
            "--schema",
            schema_name,
            "--no-input",
        ],
        capture_output=True,
        text=True,
        cwd=settings.BASE_DIR,
    )
    if result.returncode != 0:
        logger.error("Migration failed for %s: %s", schema_name, result.stderr)
        raise RuntimeError(
            f"Schema migration failed for '{schema_name}': {result.stderr}"
        )
    logger.info("Migrations complete for schema: %s", schema_name)


def _create_tenant_admin(email: str, password: str, full_name: str):
    """Create the initial admin user in the currently active tenant schema."""
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Parse name
    parts = full_name.strip().split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_staff=True,
    )

    # Assign admin role if the tenant user model has a role field
    if hasattr(user, "role"):
        user.role = "admin"
        user.save(update_fields=["role"])

    logger.info("Admin user created: %s", email)
    return user
