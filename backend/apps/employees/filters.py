"""Django Filter classes for the Employees application."""

import django_filters

from apps.employees.models import Employee, EmployeeDocument


class EmployeeFilter(django_filters.FilterSet):
    """Filter set for Employee model."""

    hired_after = django_filters.DateFilter(field_name="hire_date", lookup_expr="gte")
    hired_before = django_filters.DateFilter(field_name="hire_date", lookup_expr="lte")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Employee
        fields = [
            "status",
            "employment_type",
            "gender",
            "department",
            "designation",
            "work_location",
            "work_from_home_eligible",
        ]

    def filter_search(self, queryset, name, value):
        from apps.employees.services.search_service import EmployeeSearchService
        return EmployeeSearchService.search(queryset, value)


class EmployeeDocumentFilter(django_filters.FilterSet):
    """Filter set for EmployeeDocument model."""

    expiring_within_days = django_filters.NumberFilter(method="filter_expiring")

    class Meta:
        model = EmployeeDocument
        fields = [
            "employee",
            "document_type",
            "is_sensitive",
            "visible_to_employee",
        ]

    def filter_expiring(self, queryset, name, value):
        from datetime import date, timedelta
        expiry_threshold = date.today() + timedelta(days=int(value))
        return queryset.filter(
            expiry_date__lte=expiry_threshold,
            expiry_date__gte=date.today(),
        )
