"""Employees signals module."""

from datetime import date

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.employees.models.employee import Employee


@receiver(pre_save, sender=Employee)
def track_employment_changes(sender, instance, **kwargs):
    """Auto-create employment history when department, designation, or manager changes."""
    if not instance.pk:
        return  # Skip for new employees

    try:
        old_instance = Employee.objects.get(pk=instance.pk)
    except Employee.DoesNotExist:
        return

    from apps.employees.constants import (
        CHANGE_TYPE_ROLE_CHANGE,
        CHANGE_TYPE_TRANSFER,
    )
    from apps.employees.models.employment_history import EmploymentHistory

    # Track department change
    if old_instance.department != instance.department and (
        old_instance.department or instance.department
    ):
        EmploymentHistory.objects.create(
            employee=instance,
            effective_date=date.today(),
            change_type=CHANGE_TYPE_TRANSFER,
            from_department=old_instance.department,
            to_department=instance.department,
        )

    # Track designation change
    if old_instance.designation != instance.designation and (
        old_instance.designation or instance.designation
    ):
        EmploymentHistory.objects.create(
            employee=instance,
            effective_date=date.today(),
            change_type=CHANGE_TYPE_ROLE_CHANGE,
            from_designation=old_instance.designation,
            to_designation=instance.designation,
        )
