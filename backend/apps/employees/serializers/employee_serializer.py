"""Serializers for the Employees application."""

from rest_framework import serializers

from apps.employees.models import (
    Employee,
    EmployeeAddress,
    EmployeeBankAccount,
    EmployeeDocument,
    EmployeeFamily,
    EmergencyContact,
    EmploymentHistory,
)


# =====================================================================
# Nested / Related Serializers
# =====================================================================


class ManagerSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer for manager references (avoids circular nesting)."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = ["id", "employee_id", "full_name", "email"]
        read_only_fields = fields


class EmployeeAddressSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeAddress model."""

    class Meta:
        model = EmployeeAddress
        fields = [
            "id",
            "employee",
            "address_type",
            "line1",
            "line2",
            "city",
            "postal_code",
            "province",
            "district",
            "is_primary",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "created_on", "updated_on"]


class EmergencyContactSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyContact model."""

    class Meta:
        model = EmergencyContact
        fields = [
            "id",
            "employee",
            "name",
            "relationship",
            "phone",
            "email",
            "priority",
            "notes",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "created_on", "updated_on"]


class EmployeeFamilySerializer(serializers.ModelSerializer):
    """Serializer for EmployeeFamily model."""

    class Meta:
        model = EmployeeFamily
        fields = [
            "id",
            "employee",
            "name",
            "relationship",
            "date_of_birth",
            "occupation",
            "is_dependent",
            "phone",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "created_on", "updated_on"]


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeDocument model."""

    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee",
            "document_type",
            "title",
            "description",
            "file",
            "file_size",
            "file_type",
            "original_filename",
            "issue_date",
            "expiry_date",
            "is_sensitive",
            "visible_to_employee",
            "uploaded_by",
            "is_expired",
            "created_on",
            "updated_on",
        ]
        read_only_fields = [
            "id",
            "file_size",
            "file_type",
            "original_filename",
            "is_expired",
            "created_on",
            "updated_on",
        ]


class EmployeeBankAccountSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeBankAccount model."""

    class Meta:
        model = EmployeeBankAccount
        fields = [
            "id",
            "employee",
            "bank_name",
            "branch_name",
            "account_number",
            "account_holder_name",
            "swift_code",
            "branch_code",
            "account_type",
            "is_primary",
            "is_verified",
            "verified_by",
            "verified_at",
            "notes",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "is_verified", "verified_by", "verified_at", "created_on", "updated_on"]


class EmploymentHistorySerializer(serializers.ModelSerializer):
    """Serializer for EmploymentHistory model."""

    class Meta:
        model = EmploymentHistory
        fields = [
            "id",
            "employee",
            "effective_date",
            "change_type",
            "from_department",
            "to_department",
            "from_designation",
            "to_designation",
            "from_manager",
            "to_manager",
            "previous_salary",
            "new_salary",
            "notes",
            "changed_by",
            "created_on",
            "updated_on",
        ]
        read_only_fields = fields


# =====================================================================
# Employee Serializers (List / Detail / Create / Update)
# =====================================================================


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee list views."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "mobile",
            "department",
            "designation",
            "employment_type",
            "status",
        ]
        read_only_fields = fields


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Full serializer for employee detail views with nested data."""

    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    is_active_employee = serializers.ReadOnlyField()
    manager_detail = ManagerSummarySerializer(source="manager", read_only=True)
    addresses = EmployeeAddressSerializer(many=True, read_only=True)
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)
    family_members = EmployeeFamilySerializer(many=True, read_only=True)
    documents = EmployeeDocumentSerializer(many=True, read_only=True)
    bank_accounts = EmployeeBankAccountSerializer(many=True, read_only=True)
    employment_history = EmploymentHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "first_name",
            "last_name",
            "middle_name",
            "preferred_name",
            "full_name",
            "profile_photo",
            "nic_number",
            "date_of_birth",
            "age",
            "gender",
            "marital_status",
            "email",
            "personal_email",
            "mobile",
            "phone",
            "work_phone",
            "employment_type",
            "status",
            "department",
            "designation",
            "manager",
            "manager_detail",
            "user",
            "hire_date",
            "probation_end_date",
            "confirmation_date",
            "work_location",
            "work_from_home_eligible",
            "termination_date",
            "termination_reason",
            "exit_interview_notes",
            "resignation_date",
            "resignation_reason",
            "notice_period",
            "notes",
            "is_active_employee",
            "addresses",
            "emergency_contacts",
            "family_members",
            "documents",
            "bank_accounts",
            "employment_history",
            "created_on",
            "updated_on",
        ]
        read_only_fields = [
            "id",
            "employee_id",
            "full_name",
            "age",
            "is_active_employee",
            "created_on",
            "updated_on",
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating employees."""

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "preferred_name",
            "profile_photo",
            "nic_number",
            "date_of_birth",
            "gender",
            "marital_status",
            "email",
            "personal_email",
            "mobile",
            "phone",
            "work_phone",
            "employment_type",
            "status",
            "department",
            "designation",
            "manager",
            "hire_date",
            "probation_end_date",
            "work_location",
            "work_from_home_eligible",
            "notes",
        ]

    def validate_nic_number(self, value):
        if value and Employee.objects.filter(nic_number=value).exists():
            raise serializers.ValidationError("An employee with this NIC number already exists.")
        return value


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating employees."""

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "preferred_name",
            "profile_photo",
            "nic_number",
            "date_of_birth",
            "gender",
            "marital_status",
            "email",
            "personal_email",
            "mobile",
            "phone",
            "work_phone",
            "employment_type",
            "department",
            "designation",
            "manager",
            "work_location",
            "work_from_home_eligible",
            "notes",
        ]

    def validate_nic_number(self, value):
        if value and Employee.objects.filter(nic_number=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("An employee with this NIC number already exists.")
        return value
