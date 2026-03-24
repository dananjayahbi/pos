from django.db import models

from apps.core.mixins import TimestampMixin, UUIDMixin
from apps.organization.constants import (
    DEFAULT_MEMBERSHIP_ROLE,
    MEMBERSHIP_ROLE_CHOICES,
)


class DepartmentMember(UUIDMixin, TimestampMixin, models.Model):
    """Track employee membership in a department with role and dates.

    Maintains a full history of department assignments so that
    transfers and role changes can be audited.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="department_memberships",
        help_text="Employee who is/was a member.",
    )
    department = models.ForeignKey(
        "organization.Department",
        on_delete=models.CASCADE,
        related_name="members",
        help_text="Department the employee belongs/belonged to.",
    )
    role = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_ROLE_CHOICES,
        default=DEFAULT_MEMBERSHIP_ROLE,
        help_text="Role within the department (member, lead, deputy_manager).",
    )
    is_primary = models.BooleanField(
        default=True,
        help_text="Whether this is the employee's primary department.",
    )
    joined_date = models.DateField(
        help_text="Date the employee joined this department.",
    )
    left_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the employee left this department (null = still active).",
    )

    class Meta:
        ordering = ["-joined_date"]
        verbose_name = "Department Member"
        verbose_name_plural = "Department Members"
        indexes = [
            models.Index(fields=["employee", "department"], name="idx_dmember_emp_dept"),
            models.Index(fields=["department", "left_date"], name="idx_dmember_dept_left"),
        ]

    def __str__(self):
        status = "active" if self.left_date is None else "ended"
        return f"{self.employee} — {self.department} ({status})"

    @property
    def is_active(self):
        return self.left_date is None
