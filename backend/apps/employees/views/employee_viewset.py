"""Employee ViewSet with CRUD operations and lifecycle actions."""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.employees.models import Employee
from apps.employees.serializers import (
    EmployeeCreateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeeUpdateSerializer,
)
from apps.employees.services.employee_service import EmployeeService


class EmployeeViewSet(ModelViewSet):
    """ViewSet for Employee CRUD and lifecycle management."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "employment_type", "department", "gender"]
    search_fields = [
        "employee_id", "first_name", "last_name",
        "nic_number", "email", "mobile",
    ]
    ordering_fields = [
        "employee_id", "first_name", "last_name",
        "hire_date", "department", "created_on",
    ]
    ordering = ["-created_on"]

    def get_queryset(self):
        return Employee.objects.select_related("manager", "user")

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        if self.action == "create":
            return EmployeeCreateSerializer
        if self.action in ("update", "partial_update"):
            return EmployeeUpdateSerializer
        return EmployeeDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        return Response(
            EmployeeDetailSerializer(employee).data,
            status=status.HTTP_201_CREATED,
        )

    # ------------------------------------------------------------------
    # Custom lifecycle actions
    # ------------------------------------------------------------------

    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        """Activate an employee."""
        employee = EmployeeService.activate(pk, user=request.user)
        return Response(EmployeeDetailSerializer(employee).data)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        """Deactivate an employee."""
        reason = request.data.get("reason", "")
        employee = EmployeeService.deactivate(pk, reason=reason, user=request.user)
        return Response(EmployeeDetailSerializer(employee).data)

    @action(detail=True, methods=["post"], url_path="terminate")
    def terminate(self, request, pk=None):
        """Terminate an employee."""
        employee = EmployeeService.terminate(
            pk,
            termination_date=request.data.get("termination_date"),
            reason=request.data.get("reason", ""),
            user=request.user,
        )
        return Response(EmployeeDetailSerializer(employee).data)

    @action(detail=True, methods=["post"], url_path="resign")
    def resign(self, request, pk=None):
        """Process an employee resignation."""
        employee = EmployeeService.resign(
            pk,
            resignation_date=request.data.get("resignation_date"),
            reason=request.data.get("reason", ""),
            notice_period=request.data.get("notice_period"),
            user=request.user,
        )
        return Response(EmployeeDetailSerializer(employee).data)
