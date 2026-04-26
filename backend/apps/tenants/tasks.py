"""Celery tasks for tenant lifecycle management."""

import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(name="tenants.send_trial_reminders")
def send_trial_reminders():
    """
    Send trial expiry reminder emails.
    Run: daily at midnight via Celery Beat.
    """
    # Import here to avoid circular imports at module load time
    from apps.tenants.models import Tenant

    today = timezone.now().date()
    reminder_days = [3, 1]

    sent_count = 0
    for days_left in reminder_days:
        expiry_date = today + timedelta(days=days_left)
        expiring_tenants = Tenant.objects.filter(
            on_trial=True,
            paid_until=expiry_date,
            status="active",
        )
        for tenant in expiring_tenants:
            if not tenant.contact_email:
                continue
            try:
                send_mail(
                    subject=f"Your free trial expires in {days_left} day(s)",
                    message=(
                        f"Hi {tenant.contact_name},\n\n"
                        f"Your trial for {tenant.name} expires on {expiry_date}.\n"
                        f"Please upgrade your subscription to continue using the system.\n\n"
                        f"If you have questions, contact our support team.\n\n"
                        f"The Team"
                    ),
                    from_email=None,  # uses DEFAULT_FROM_EMAIL
                    recipient_list=[tenant.contact_email],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(
                    "Trial reminder sent: tenant=%s days_left=%d",
                    tenant.slug,
                    days_left,
                )
            except Exception as exc:
                logger.error(
                    "Failed to send trial reminder to %s: %s",
                    tenant.contact_email,
                    exc,
                )

    logger.info("Trial reminders sent: %d", sent_count)
    return {"sent": sent_count}


@shared_task(name="tenants.suspend_expired_trials")
def suspend_expired_trials():
    """
    Suspend tenants whose trial has expired.
    Run: daily at 00:05 via Celery Beat (5 min after reminders).
    Grace period: 1 day after paid_until.
    """
    from apps.tenants.models import Tenant

    today = timezone.now().date()
    # Suspend if trial expired yesterday or earlier (1 day grace)
    grace_cutoff = today - timedelta(days=1)

    expired_tenants = Tenant.objects.filter(
        on_trial=True,
        paid_until__lte=grace_cutoff,
        status="active",
    )

    suspended_count = 0
    for tenant in expired_tenants:
        try:
            tenant.status = "suspended"
            tenant.save(update_fields=["status"])
            suspended_count += 1

            logger.info(
                "Trial expired — tenant suspended: %s (paid_until=%s)",
                tenant.slug,
                tenant.paid_until,
            )

            # Notify tenant
            if tenant.contact_email:
                send_mail(
                    subject=f"Your {tenant.name} account has been suspended",
                    message=(
                        f"Hi {tenant.contact_name},\n\n"
                        f"Your free trial has expired and your account has been suspended.\n"
                        f"Your data is preserved. Please upgrade to reactivate your account.\n\n"
                        f"The Team"
                    ),
                    from_email=None,
                    recipient_list=[tenant.contact_email],
                    fail_silently=True,
                )

        except Exception as exc:
            logger.error("Failed to suspend tenant %s: %s", tenant.slug, exc)

    logger.info("Expired trials suspended: %d", suspended_count)
    return {"suspended": suspended_count}
