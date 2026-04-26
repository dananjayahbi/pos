"""
Celery tasks for the analytics application.

Handles asynchronous report generation and scheduled report processing.
"""

import logging

from celery import shared_task
from django.utils import timezone
from django_tenants.utils import get_tenant_model, schema_context

logger = logging.getLogger(__name__)


@shared_task(name="analytics.process_scheduled_reports")
def process_scheduled_reports():
    """
    Find and execute all scheduled reports that are due across all tenants.

    This task should be called periodically (e.g. every minute via
    Celery Beat) to process overdue schedules.
    """
    from apps.analytics.models import ScheduledReport
    from apps.analytics.services.scheduler import ReportSchedulerService

    now = timezone.now()
    TenantModel = get_tenant_model()
    total_processed = 0
    total_failed = 0

    for tenant in TenantModel.objects.exclude(schema_name="public"):
        with schema_context(tenant.schema_name):
            due = ScheduledReport.objects.filter(
                is_active=True,
                next_run__lte=now,
            ).select_related(
                "saved_report",
                "saved_report__report_definition",
            )

            processed = 0
            failed = 0
            for schedule in due:
                result = ReportSchedulerService.execute(schedule)
                if result["success"]:
                    processed += 1
                else:
                    failed += 1

            if processed or failed:
                logger.info(
                    "Scheduled reports [tenant=%s]: %d processed, %d failed",
                    tenant.schema_name,
                    processed,
                    failed,
                )
            total_processed += processed
            total_failed += failed

    return {"processed": total_processed, "failed": total_failed}
