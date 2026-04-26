"""
Celery tasks for invoice email operations.
"""

import logging

from celery import shared_task
from django_tenants.utils import get_tenant_model, schema_context

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_invoice_email_task(self, tenant_schema: str, invoice_id):
    """Send invoice email asynchronously."""
    try:
        from apps.invoices.services.email_service import InvoiceEmailService
        with schema_context(tenant_schema):
            InvoiceEmailService.send_invoice_email(invoice_id)
    except Exception as exc:
        logger.error("Failed to send invoice email for %s: %s", invoice_id, exc)
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_reminder_email_task(self, tenant_schema: str, invoice_id):
    """Send payment reminder email asynchronously."""
    try:
        from apps.invoices.services.email_service import InvoiceEmailService
        with schema_context(tenant_schema):
            InvoiceEmailService.send_reminder_email(invoice_id)
    except Exception as exc:
        logger.error("Failed to send reminder for %s: %s", invoice_id, exc)
        self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_overdue_email_task(self, tenant_schema: str, invoice_id):
    """Send overdue notification email asynchronously."""
    try:
        from apps.invoices.services.email_service import InvoiceEmailService
        with schema_context(tenant_schema):
            InvoiceEmailService.send_overdue_email(invoice_id)
    except Exception as exc:
        logger.error("Failed to send overdue notice for %s: %s", invoice_id, exc)
        self.retry(exc=exc)


@shared_task
def send_overdue_reminders():
    """Batch task: send overdue emails for all overdue invoices across all tenants."""
    from apps.invoices.constants import InvoiceStatus
    from apps.invoices.models import Invoice

    TenantModel = get_tenant_model()
    total_count = 0

    for tenant in TenantModel.objects.exclude(schema_name="public"):
        with schema_context(tenant.schema_name):
            overdue = Invoice.objects.filter(status=InvoiceStatus.OVERDUE, is_deleted=False)
            count = 0
            for inv in overdue:
                if inv.customer_email:
                    send_overdue_email_task.delay(tenant.schema_name, str(inv.id))
                    count += 1
            if count:
                logger.info(
                    "Queued %d overdue reminder emails for tenant=%s",
                    count, tenant.schema_name,
                )
            total_count += count

    logger.info("Queued %d overdue reminder emails total", total_count)
