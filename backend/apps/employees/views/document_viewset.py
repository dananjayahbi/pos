"""Document ViewSet for employee document management."""

from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.employees.models import EmployeeDocument
from apps.employees.serializers import EmployeeDocumentSerializer


class DocumentViewSet(ModelViewSet):
    """ViewSet for Employee Documents with upload support."""

    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeDocumentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["employee", "document_type", "is_sensitive"]
    search_fields = ["title", "description", "employee__first_name", "employee__last_name"]
    ordering_fields = ["created_on", "expiry_date", "document_type"]
    ordering = ["-created_on"]

    def get_queryset(self):
        return EmployeeDocument.objects.select_related("employee", "uploaded_by")

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
