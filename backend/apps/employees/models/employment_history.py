"""EmploymentHistory model for the Employees application."""

from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.core.mixins import TimestampMixin, UUIDMixin
from apps.employees.constants import CHANGE_TYPE_CHOICES


class EmploymentHistory(UUIDMixin, TimestampMixin, models.Model):
    """
    Audit trail for employment changes.

    Tracks promotions, transfers, demotions, salary changes,
    and role changes throughout an employee's career.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="employment_history",
        verbose_name="Employee",
        help_text="Employee this history entry belongs to.",
    )

    # ── Change Details ──────────────────────────────────────────────
    effective_date = models.DateField(
        db_index=True,
        verbose_name="Effective Date",
        help_text="Date when the change became effective.",
    )
    change_type = models.CharField(
        max_length=20,
        choices=CHANGE_TYPE_CHOICES,
        verbose_name="Change Type",
        help_text="Type of employment change.",
    )

    # ── Department Change ───────────────────────────────────────────
    from_department = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="From Department",
    )
    to_department = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="To Department",
    )

    # ── Designation Change ──────────────────────────────────────────
    from_designation = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="From Designation",
    )
    to_designation = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="To Designation",
    )

    # ── Manager Change ──────────────────────────────────────────────
    from_manager = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_from_manager",
        verbose_name="Previous Manager",
    )
    to_manager = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_to_manager",
        verbose_name="New Manager",
    )

    # ── Salary Change ───────────────────────────────────────────────
    previous_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Previous Salary",
    )
    new_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="New Salary",
    )

    # ── Notes ───────────────────────────────────────────────────────
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notes",
        help_text="Additional notes about this change.",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_changes_made",
        verbose_name="Changed By",
        help_text="User who made this change.",
    )

    class Meta:
        db_table = "employees_employment_history"
        verbose_name = "Employment History"
        verbose_name_plural = "Employment Histories"
        ordering = ["-effective_date"]
        indexes = [
            models.Index(
                fields=["employee", "effective_date"],
                name="idx_emp_hist_date",
            ),
            models.Index(
                fields=["change_type"],
                name="idx_emp_hist_type",
            ),
        ]

    def __str__(self):
        return (
            f"{self.employee.full_name} - "
            f"{self.get_change_type_display()} - "
            f"{self.effective_date}"
        )
