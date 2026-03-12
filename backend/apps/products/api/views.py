"""
Category views for the products API.

Provides a full CRUD ViewSet with custom tree endpoint.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Brand, Category, Product, TaxClass, UnitOfMeasure

from .filters import ProductFilter
from .serializers import (
    BrandSerializer,
    CategoryCreateUpdateSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
    CategoryTreeSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    TaxClassSerializer,
    UnitOfMeasureSerializer,
)


class CategoryViewSet(ModelViewSet):
    """
    ViewSet for product categories.

    Endpoints
    ---------
    GET    /api/v1/categories/          — list
    POST   /api/v1/categories/          — create
    GET    /api/v1/categories/{id}/     — retrieve
    PUT    /api/v1/categories/{id}/     — update
    PATCH  /api/v1/categories/{id}/     — partial_update
    DELETE /api/v1/categories/{id}/     — destroy
    GET    /api/v1/categories/tree/     — tree (custom)
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["parent", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "display_order", "created_on"]
    ordering = ["display_order", "name"]

    # ── QuerySet ────────────────────────────────────────────────────

    def get_queryset(self):
        """
        Return categories for the current tenant.

        For list actions the queryset is optimised with
        ``select_related``.  The ``DjangoFilterBackend`` handles
        ``parent`` and ``is_active`` query-parameter filtering.
        """
        return Category.objects.all().select_related("parent")

    # ── Serializer selection ────────────────────────────────────────

    def get_serializer_class(self):
        """Return the appropriate serializer for the current action."""
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "retrieve":
            return CategoryDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return CategoryCreateUpdateSerializer
        if self.action == "tree":
            return CategoryTreeSerializer
        return CategoryListSerializer

    # ── Custom actions ──────────────────────────────────────────────

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        """
        Return the complete category tree (or a subtree).

        Query params:
            active_only (bool): ``true`` (default) to include only
                active categories.
            root_id (uuid, optional): Return only the subtree rooted
                at this category.
        """
        active_only = (
            request.query_params.get("active_only", "true").lower()
            in ("true", "1", "yes")
        )
        root_id = request.query_params.get("root_id")
        if root_id:
            try:
                root_node = Category.objects.get(pk=root_id)
            except Category.DoesNotExist:
                return Response(
                    {"detail": "Root category not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = CategoryTreeSerializer(root_node)
            return Response(serializer.data)
        root_qs = Category.objects.get_tree(active_only=active_only)
        serializer = CategoryTreeSerializer(root_qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="move")
    def move(self, request, pk=None):
        """
        Move category to a new parent or position.

        Body:
            target (uuid|null): Target parent ID (null → make root).
            position (str): ``'first-child'``, ``'last-child'``,
                ``'left'``, ``'right'``. Default ``'last-child'``.
        """
        category = self.get_object()
        target_id = request.data.get("target")
        position = request.data.get("position", "last-child")

        if position not in ("first-child", "last-child", "left", "right"):
            return Response(
                {"detail": "Invalid position."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target = None
        if target_id is not None:
            try:
                target = Category.objects.get(pk=target_id)
            except Category.DoesNotExist:
                return Response(
                    {"detail": "Target category not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        try:
            Category.objects.move_node(category, target, position=position)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)


class BrandViewSet(ModelViewSet):
    """
    ViewSet for product brands.

    Endpoints
    ---------
    GET    /api/v1/brands/          — list
    POST   /api/v1/brands/          — create
    GET    /api/v1/brands/{id}/     — retrieve
    PUT    /api/v1/brands/{id}/     — update
    PATCH  /api/v1/brands/{id}/     — partial_update
    DELETE /api/v1/brands/{id}/     — destroy
    """

    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name"]


class TaxClassViewSet(ModelViewSet):
    """
    ViewSet for tax classes.

    Endpoints
    ---------
    GET    /api/v1/tax-classes/          — list
    POST   /api/v1/tax-classes/          — create
    GET    /api/v1/tax-classes/{id}/     — retrieve
    PUT    /api/v1/tax-classes/{id}/     — update
    PATCH  /api/v1/tax-classes/{id}/     — partial_update
    DELETE /api/v1/tax-classes/{id}/     — destroy
    """

    queryset = TaxClass.objects.all()
    serializer_class = TaxClassSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_default"]


class ProductViewSet(ModelViewSet):
    """
    ViewSet for products.

    Endpoints
    ---------
    GET    /api/v1/products/              — list
    POST   /api/v1/products/              — create
    GET    /api/v1/products/{id}/         — retrieve
    PUT    /api/v1/products/{id}/         — update
    PATCH  /api/v1/products/{id}/         — partial_update
    DELETE /api/v1/products/{id}/         — destroy
    GET    /api/v1/products/published/    — published (custom)
    GET    /api/v1/products/featured/     — featured (custom)
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "sku", "barcode", "description"]
    ordering_fields = ["name", "created_on", "updated_on", "selling_price"]
    ordering = ["-created_on"]

    def get_queryset(self):
        """Return products with related objects pre-fetched."""
        return Product.objects.select_related(
            "category", "brand", "tax_class", "unit_of_measure"
        )

    def get_serializer_class(self):
        """Return the appropriate serializer for the current action."""
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductCreateSerializer

    @action(detail=False, methods=["get"], url_path="published")
    def published(self, request):
        """Return published products (active + webstore visible)."""
        queryset = self.get_queryset().published()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        """Return featured active products."""
        queryset = self.get_queryset().active().featured()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)
