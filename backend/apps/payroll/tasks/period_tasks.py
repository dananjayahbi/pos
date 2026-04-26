"""Celery tasks for automatic payroll period management."""

import calendar
import logging
from datetime import date

from celery import shared_task
from django_tenants.utils import get_tenant_model, schema_context

logger = logging.getLogger(__name__)


@shared_task(
    name="payroll.auto_create_payroll_periods",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def auto_create_payroll_periods(self):
    """Auto-create payroll periods for tenants with auto_create_period enabled.

    Runs daily (scheduled via Celery Beat). Iterates all active tenants
    and creates payroll periods for any PayrollSettings configured for
    auto-creation on today's date.
    """
    from apps.payroll.constants import PayrollStatus
    from apps.payroll.models.payroll_period import PayrollPeriod
    from apps.payroll.models.payroll_settings import PayrollSettings

    TenantModel = get_tenant_model()
    today = date.today()
    total_tenants_checked = 0
    total_periods_created = 0
    all_errors = []

    for tenant in TenantModel.objects.exclude(schema_name="public"):
        with schema_context(tenant.schema_name):
            settings_qs = PayrollSettings.objects.filter(
                auto_create_period=True,
                auto_create_day=today.day,
            )

            tenants_checked = 0
            periods_created = 0
            errors = []

            for ps in settings_qs:
                tenants_checked += 1
                try:
                    months_ahead = ps.create_months_ahead or 1

                    for offset in range(months_ahead + 1):
                        month = today.month + offset
                        year = today.year
                        while month > 12:
                            month -= 12
                            year += 1

                        # Skip if period already exists
                        if PayrollPeriod.objects.filter(
                            period_month=month, period_year=year
                        ).exists():
                            continue

                        # Calculate dates
                        start_date, end_date = ps.calculate_cutoff_dates(month, year)
                        pay_date = ps.calculate_pay_date(month, year)

                        # Calculate working days
                        last_day = calendar.monthrange(year, month)[1]

                        PayrollPeriod.objects.create(
                            period_month=month,
                            period_year=year,
                            start_date=start_date,
                            end_date=end_date,
                            pay_date=pay_date,
                            status=PayrollStatus.DRAFT,
                        )
                        periods_created += 1
                        logger.info(
                            "Created payroll period %s/%s for tenant=%s (pay date: %s)",
                            month, year, tenant.schema_name, pay_date,
                        )

                except Exception:
                    msg = f"Error creating periods for PayrollSettings {ps.pk} (tenant={tenant.schema_name})"
                    logger.exception(msg)
                    errors.append(msg)

            total_tenants_checked += tenants_checked
            total_periods_created += periods_created
            all_errors.extend(errors)

    result = {
        "tenants_checked": total_tenants_checked,
        "periods_created": total_periods_created,
        "errors": all_errors,
    }
    logger.info("auto_create_payroll_periods completed: %s", result)
    return result
