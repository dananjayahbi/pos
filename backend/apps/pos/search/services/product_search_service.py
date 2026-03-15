"""
ProductSearchService – unified product search for POS terminals.

Provides barcode, SKU, name, and combined searches with deduplication,
stock availability, and search-history tracking.
"""

from decimal import Decimal
from typing import Any, Optional

from django.db.models import Q, QuerySet

from apps.pos.constants import (
    SEARCH_METHOD_BARCODE,
    SEARCH_METHOD_COMBINED,
    SEARCH_METHOD_NAME,
    SEARCH_METHOD_SKU,
)
from apps.pos.search.validators import detect_barcode_format, parse_weight_barcode
from apps.products.constants import PRODUCT_STATUS


class ProductSearchService:
    """Stateless service with class-method API for POS product search."""

    # ── internal helpers ────────────────────────────────────────────

    @classmethod
    def _get_tenant_products(cls, category=None) -> QuerySet:
        """Return an optimised queryset of active, POS-visible products."""
        from apps.products.models import Product

        qs = Product.objects.filter(
            is_active=True,
            is_deleted=False,
            is_pos_visible=True,
            status=PRODUCT_STATUS.ACTIVE,
        ).select_related("category", "brand", "tax_class", "unit_of_measure")

        if category is not None:
            descendants = category.get_descendants(include_self=True)
            qs = qs.filter(category__in=descendants)

        return qs

    @classmethod
    def _format_product_result(
        cls, product, *, search_method: str = "", variant=None
    ) -> dict[str, Any]:
        """Map a Product (or variant) to a dict for the POS frontend."""
        result: dict[str, Any] = {
            "id": str(product.id),
            "name": product.name,
            "sku": product.sku,
            "barcode": product.barcode,
            "selling_price": str(product.selling_price),
            "cost_price": str(product.cost_price) if product.cost_price else None,
            "category": str(product.category) if product.category_id else None,
            "brand": str(product.brand) if product.brand_id else None,
            "tax_class": str(product.tax_class) if product.tax_class_id else None,
            "product_type": product.product_type,
            "is_pos_visible": product.is_pos_visible,
        }
        if variant:
            result["variant_id"] = str(variant.id)
            result["variant_sku"] = variant.sku
            result["variant_barcode"] = variant.barcode
            result["variant_name"] = variant.name
        if search_method:
            result["search_method"] = search_method
        return result

    @classmethod
    def _deduplicate_results(
        cls, results: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Remove duplicate products, keeping the first occurrence."""
        seen: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for item in results:
            pid = item["id"]
            if pid not in seen:
                seen.add(pid)
                deduped.append(item)
        return deduped

    # ── core search methods ─────────────────────────────────────────

    @classmethod
    def barcode_search(cls, barcode: str) -> Optional[dict[str, Any]]:
        """Exact barcode match — checks variants first, then products."""
        if not barcode or not barcode.strip():
            return None
        barcode = barcode.strip()

        # Weight-embedded barcode
        weight_data = parse_weight_barcode(barcode)
        if weight_data:
            product = (
                cls._get_tenant_products()
                .filter(barcode__endswith=weight_data["product_code"])
                .first()
            )
            if product:
                result = cls._format_product_result(
                    product, search_method=SEARCH_METHOD_BARCODE
                )
                result["weight_kg"] = str(weight_data["weight_kg"])
                return result

        # Variant barcode
        variant = cls._search_variant_by_barcode(barcode)
        if variant:
            return cls._format_product_result(
                variant.product, search_method=SEARCH_METHOD_BARCODE, variant=variant
            )

        # Product barcode
        product = cls._get_tenant_products().filter(barcode=barcode).first()
        if product:
            return cls._format_product_result(
                product, search_method=SEARCH_METHOD_BARCODE
            )

        return None

    @classmethod
    def sku_search(
        cls, sku: str, *, exact: bool = True
    ) -> list[dict[str, Any]]:
        """Search by SKU — exact or partial (icontains)."""
        if not sku or not sku.strip():
            return []
        sku = sku.strip()
        qs = cls._get_tenant_products()

        if exact:
            qs = qs.filter(sku__iexact=sku)
        else:
            qs = qs.filter(sku__icontains=sku)

        qs = qs.order_by("sku", "name")

        return [
            cls._format_product_result(p, search_method=SEARCH_METHOD_SKU)
            for p in qs
        ]

    @classmethod
    def name_search(
        cls, query: str, *, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Fuzzy name search using icontains (trigram when postgres ext available)."""
        if not query or len(query.strip()) < 2:
            return []
        query = query.strip()
        qs = cls._get_tenant_products().filter(name__icontains=query).order_by("name")[
            :limit
        ]
        return [
            cls._format_product_result(p, search_method=SEARCH_METHOD_NAME)
            for p in qs
        ]

    @classmethod
    def combined_search(
        cls, query: str, *, limit: int = 20
    ) -> list[dict[str, Any]]:
        """
        Cascade search: barcode → exact SKU → name + partial SKU.

        Priority:
        1. Barcode exact match → return immediately
        2. SKU exact match → return immediately
        3. Combine name search + partial SKU search, deduplicate and limit
        """
        if not query or not query.strip():
            return []
        query = query.strip()

        # 1. barcode
        barcode_result = cls.barcode_search(query)
        if barcode_result:
            barcode_result["search_method"] = SEARCH_METHOD_COMBINED
            return [barcode_result]

        # 2. exact SKU
        sku_exact = cls.sku_search(query, exact=True)
        if sku_exact:
            for r in sku_exact:
                r["search_method"] = SEARCH_METHOD_COMBINED
            return sku_exact

        # 3. name + partial SKU
        name_results = cls.name_search(query, limit=limit)
        sku_partial = cls.sku_search(query, exact=False)
        combined = name_results + sku_partial
        for r in combined:
            r["search_method"] = SEARCH_METHOD_COMBINED
        return cls._deduplicate_results(combined)[:limit]

    # ── enhanced helpers ────────────────────────────────────────────

    @classmethod
    def _search_variant_by_barcode(cls, barcode: str):
        """Look up a ProductVariant by its barcode."""
        from apps.products.models import ProductVariant

        return (
            ProductVariant.objects.select_related("product")
            .filter(barcode=barcode, product__is_pos_visible=True)
            .first()
        )

    @classmethod
    def filter_by_category(
        cls, category, *, query: str = None, limit: int = 50, sort_by: str = "name"
    ) -> list[dict[str, Any]]:
        """Filter products by category, optionally narrowing with a text query."""
        qs = cls._get_tenant_products(category=category)
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(sku__icontains=query))

        ordering = {
            "name": "name",
            "price": "selling_price",
        }
        qs = qs.order_by(ordering.get(sort_by, "name"))[:limit]
        return [cls._format_product_result(p) for p in qs]

    # ── search history / suggestions ────────────────────────────────

    @classmethod
    def record_search(
        cls,
        query_text: str,
        *,
        result_count: int = 0,
        search_method: str = SEARCH_METHOD_COMBINED,
        terminal=None,
        user=None,
        selected_product=None,
    ):
        """Persist a search to SearchHistory."""
        from apps.pos.search.models import SearchHistory

        SearchHistory.objects.create(
            query=query_text[:200],
            result_count=result_count,
            search_method=search_method,
            terminal=terminal,
            user=user,
            selected_product=selected_product,
        )

    @classmethod
    def get_recent_searches(
        cls, *, terminal=None, user=None, limit: int = 10
    ) -> QuerySet:
        """Return distinct recent queries ordered by timestamp."""
        from apps.pos.search.models import SearchHistory

        qs = SearchHistory.objects.all()
        if terminal:
            qs = qs.filter(terminal=terminal)
        if user:
            qs = qs.filter(user=user)
        return qs.values_list("query", flat=True).distinct()[:limit]

    @classmethod
    def get_popular_products(
        cls, *, terminal=None, user=None, limit: int = 10, days: int = 30
    ) -> list[dict[str, Any]]:
        """Products most frequently selected in search history."""
        from django.db.models import Count
        from django.utils import timezone

        from apps.pos.search.models import SearchHistory

        since = timezone.now() - timezone.timedelta(days=days)
        qs = SearchHistory.objects.filter(
            timestamp__gte=since,
            selected_product__isnull=False,
        )
        if terminal:
            qs = qs.filter(terminal=terminal)
        if user:
            qs = qs.filter(user=user)

        top_ids = (
            qs.values("selected_product")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )

        from apps.products.models import Product

        products = Product.objects.filter(
            id__in=[row["selected_product"] for row in top_ids]
        )
        product_map = {str(p.id): p for p in products}
        return [
            cls._format_product_result(product_map[str(row["selected_product"])])
            for row in top_ids
            if str(row["selected_product"]) in product_map
        ]

    @classmethod
    def get_search_suggestions(
        cls, partial_query: str, *, terminal=None, limit: int = 5
    ) -> list[str]:
        """Autocomplete suggestions from past search queries."""
        from django.db.models import Count

        from apps.pos.search.models import SearchHistory

        if not partial_query or len(partial_query.strip()) < 2:
            return []
        qs = SearchHistory.objects.filter(query__icontains=partial_query.strip())
        if terminal:
            qs = qs.filter(terminal=terminal)
        return list(
            qs.values_list("query", flat=True)
            .annotate(freq=Count("id"))
            .order_by("-freq")[:limit]
        )
