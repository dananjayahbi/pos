"""Employee model for the Employees application."""

from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin
from apps.employees.constants import (
    DEFAULT_EMPLOYEE_STATUS,
    DEFAULT_EMPLOYMENT_TYPE,
    EMPLOYEE_STATUS_ACTIVE,
    EMPLOYEE_STATUS_CHOICES,
    EMPLOYEE_STATUS_INACTIVE,
    EMPLOYEE_STATUS_ON_LEAVE,
    EMPLOYEE_STATUS_RESIGNED,
    EMPLOYEE_STATUS_TERMINATED,
    EMPLOYMENT_TYPE_CHOICES,
    GENDER_CHOICES,
    MARITAL_STATUS_CHOICES,
)
from apps.employees.validators.nic_validator import validate_nic


def employee_photo_path(instance, filename):
    """Generate upload path for employee profile photos."""
    return f"employees/photos/{instance.employee_id}/{filename}"


class Employee(UUIDMixin, TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Comprehensive employee record within a tenant organisation.

    Stores personal information, employment details, and links to
    user accounts. Employee ID is auto-generated in EMP-XXXX format.
    """

    # ── Employee ID ─────────────────────────────────────────────────
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True,
        verbose_name="Employee ID",
        help_text="Auto-generated employee identifier (EMP-0001 format).",
    )

    # ── User Link (Optional) ───────────────────────────────────────
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee",
        verbose_name="User Account",
        help_text="Optional link to a user account for system access.",
    )

    # ── Name Fields ─────────────────────────────────────────────────
    first_name = models.CharField(
        max_length=100,
        verbose_name="First Name",
        help_text="Employee's given name.",
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Last Name",
        help_text="Employee's family name.",
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Middle Name",
        help_text="Employee's middle name or initial.",
    )
    preferred_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Preferred Name",
        help_text="Nickname or preferred name for informal use.",
    )

    # ── Profile Photo ───────────────────────────────────────────────
    profile_photo = models.ImageField(
        upload_to=employee_photo_path,
        blank=True,
        null=True,
        verbose_name="Profile Photo",
        help_text="Employee's profile photograph.",
    )

    # ── NIC (National Identity Card) ────────────────────────────────
    nic_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        validators=[validate_nic],
        verbose_name="NIC Number",
        help_text="Sri Lanka NIC number (old: 912345678V, new: 199112345678).",
    )

    # ── Date of Birth ───────────────────────────────────────────────
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth",
        help_text="Employee's date of birth.",
    )

    # ── Gender ──────────────────────────────────────────────────────
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        default="",
        verbose_name="Gender",
        help_text="Employee's gender.",
    )

    # ── Marital Status ──────────────────────────────────────────────
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        default="",
        verbose_name="Marital Status",
        help_text="Employee's marital status.",
    )

    # ── Contact Fields ──────────────────────────────────────────────
    email = models.EmailField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Work Email",
        help_text="Official work email address.",
    )
    personal_email = models.EmailField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Personal Email",
        help_text="Personal email address (optional).",
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Mobile Phone",
        help_text="Mobile number in +94 XX XXX XXXX format.",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Phone (Landline)",
        help_text="Home or landline number.",
    )
    work_phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Work Phone",
        help_text="Office/work phone number.",
    )

    # ── Employment Type ─────────────────────────────────────────────
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=DEFAULT_EMPLOYMENT_TYPE,
        db_index=True,
        verbose_name="Employment Type",
        help_text="Type of employment (full-time, part-time, contract, etc.).",
    )

    # ── Status ──────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=EMPLOYEE_STATUS_CHOICES,
        default=DEFAULT_EMPLOYEE_STATUS,
        db_index=True,
        verbose_name="Status",
        help_text="Current employment status.",
    )

    # ── Department & Designation (string for now, FK in SP02) ──────
    department = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Department",
        help_text="Department name (will be FK in SubPhase-02).",
    )
    designation = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Designation",
        help_text="Job title/designation (will be FK in SubPhase-02).",
    )

    # ── Manager (Self-referential FK) ───────────────────────────────
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
        verbose_name="Manager",
        help_text="Direct manager/reporting supervisor.",
    )

    # ── Employment Dates ────────────────────────────────────────────
    hire_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Hire Date",
        help_text="Date the employee joined the organisation.",
    )
    probation_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Probation End Date",
        help_text="Date probation period ends.",
    )
    confirmation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Confirmation Date",
        help_text="Date of employment confirmation after probation.",
    )

    # ── Work Location ───────────────────────────────────────────────
    work_location = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Work Location",
        help_text="Office or work location name.",
    )
    work_from_home_eligible = models.BooleanField(
        default=False,
        verbose_name="WFH Eligible",
        help_text="Whether employee is eligible for work from home.",
    )

    # ── Termination Fields ──────────────────────────────────────────
    termination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Termination Date",
        help_text="Date employment was terminated.",
    )
    termination_reason = models.TextField(
        blank=True,
        default="",
        verbose_name="Termination Reason",
        help_text="Reason for termination.",
    )
    exit_interview_notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Exit Interview Notes",
        help_text="Notes from exit interview.",
    )

    # ── Resignation Fields ──────────────────────────────────────────
    resignation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Resignation Date",
        help_text="Date resignation was submitted.",
    )
    resignation_reason = models.TextField(
        blank=True,
        default="",
        verbose_name="Resignation Reason",
        help_text="Reason for resignation.",
    )
    notice_period = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Notice Period (Days)",
        help_text="Notice period in days.",
    )

    # ── Notes ───────────────────────────────────────────────────────
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notes",
        help_text="Internal HR notes about this employee.",
    )

    class Meta:
        db_table = "employees_employee"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["employee_id"]
        indexes = [
            models.Index(
                fields=["employee_id"],
                name="idx_emp_employee_id",
            ),
            models.Index(
                fields=["status"],
                name="idx_emp_status",
            ),
            models.Index(
                fields=["nic_number"],
                name="idx_emp_nic_number",
            ),
            models.Index(
                fields=["last_name", "first_name"],
                name="idx_emp_name",
            ),
            models.Index(
                fields=["employment_type", "status"],
                name="idx_emp_type_status",
            ),
        ]

    def __str__(self):
        return f"{self.employee_id}: {self.full_name}"

    @property
    def full_name(self):
        """Return the employee's full name."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)

    def get_display_name(self):
        """Return preferred name if set, otherwise full name."""
        return self.preferred_name if self.preferred_name else self.full_name

    @property
    def age(self):
        """Calculate current age in years from date_of_birth."""
        if not self.date_of_birth:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            years -= 1
        return years

    @property
    def is_minor(self):
        """Return True if employee is under 18."""
        if self.age is None:
            return None
        return self.age < 18

    @property
    def is_active_employee(self):
        """Return True if employee status is active."""
        return self.status == EMPLOYEE_STATUS_ACTIVE

    @property
    def is_terminated(self):
        """Return True if employee is terminated."""
        return self.status == EMPLOYEE_STATUS_TERMINATED

    @property
    def is_resigned(self):
        """Return True if employee has resigned."""
        return self.status == EMPLOYEE_STATUS_RESIGNED

    def clean(self):
        """Validate model data."""
        super().clean()
        errors = {}

        # Validate DOB not in future
        if self.date_of_birth and self.date_of_birth > date.today():
            errors["date_of_birth"] = "Date of birth cannot be in the future."

        # Validate minimum working age (16 years)
        if self.date_of_birth:
            today = date.today()
            age_years = today.year - self.date_of_birth.year
            if (today.month, today.day) < (
                self.date_of_birth.month,
                self.date_of_birth.day,
            ):
                age_years -= 1
            if age_years < 16:
                errors["date_of_birth"] = (
                    "Employee must be at least 16 years old."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Auto-generate employee_id if not set."""
        if not self.employee_id:
            self.employee_id = self._generate_employee_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_employee_id(cls):
        """Generate the next employee ID in EMP-XXXX format."""
        from apps.employees.constants import (
            EMPLOYEE_ID_PADDING,
            EMPLOYEE_ID_PREFIX,
        )

        last_employee = (
            cls.objects.order_by("-employee_id")
            .values_list("employee_id", flat=True)
            .first()
        )
        if last_employee:
            try:
                last_number = int(last_employee.split("-")[-1])
            except (ValueError, IndexError):
                last_number = 0
        else:
            last_number = 0

        next_number = last_number + 1
        return f"{EMPLOYEE_ID_PREFIX}-{str(next_number).zfill(EMPLOYEE_ID_PADDING)}"
