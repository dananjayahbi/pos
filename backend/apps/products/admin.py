"""
Django admin configuration for the Products application.

Provides tree-based admin interface for Category model using
MPTTModelAdmin with drag-drop reordering, search, filters,
and organized fieldsets.
"""

from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from apps.products.models import Brand, Category, Product, TaxClass, UnitOfMeasure


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    Admin configuration for Category model with MPTT tree display.

    Features:
        - Hierarchical tree display with indentation
        - Drag-drop reordering via MPTTModelAdmin
        - Auto-populated slug from name
        - Organized fieldsets (Basic Info, Display, SEO, Timestamps)
        - Sidebar filters for quick category filtering
        - Full-text search across name, slug, and description
    """

    # ── List View Configuration ─────────────────────────────────────
    list_display = [
        "name",
        "slug",
        "parent",
        "is_active",
        "display_order",
        "children_count",
        "created_on",
    ]
    list_display_links = ["name"]
    list_editable = ["is_active", "display_order"]
    list_filter = [
        "is_active",
        "level",
        "parent",
        "created_on",
        "updated_on",
    ]
    list_per_page = 50

    # ── Search ──────────────────────────────────────────────────────
    search_fields = ["name", "slug", "description"]

    # ── Auto-populate slug from name ────────────────────────────────
    prepopulated_fields = {"slug": ("name",)}

    # ── Ordering (tree_id, lft for proper MPTT tree order) ──────────
    ordering = ["tree_id", "lft"]

    # ── Read-only timestamp fields ──────────────────────────────────
    readonly_fields = ["created_on", "updated_on"]

    # ── MPTT-specific: pixel indentation per tree level ─────────────
    mptt_level_indent = 20

    # ── Fieldsets for organized form layout ─────────────────────────
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("name", "slug", "parent", "description"),
            },
        ),
        (
            "Display",
            {
                "fields": ("image", "icon", "is_active", "display_order"),
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": ("seo_title", "seo_description", "seo_keywords"),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_on", "updated_on"),
            },
        ),
    )

    # ── Custom list columns ─────────────────────────────────────────

    @admin.display(description="Children", ordering="lft")
    def children_count(self, obj):
        """Return the number of direct children for the list view."""
        return obj.get_children().count()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin configuration for Brand model.

    Features:
        - Logo preview in detail view
        - Auto-populated slug from name
        - Organized fieldsets
    """

    list_display = ["name", "logo_preview", "is_active", "created_on"]
    list_filter = ["is_active", "created_on"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["logo_preview", "created_on", "updated_on"]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("name", "slug", "description"),
            },
        ),
        (
            "Branding",
            {
                "fields": ("logo", "logo_preview", "website"),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_on", "updated_on"),
            },
        ),
    )

    @admin.display(description="Logo Preview")
    def logo_preview(self, obj):
        """Show a small logo thumbnail if the brand has a logo."""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.logo.url,
            )
        return "-"


@admin.register(TaxClass)
class TaxClassAdmin(admin.ModelAdmin):
    """
    Admin configuration for TaxClass model.

    Features:
        - Rate display with percentage symbol
        - Default tax class indicator
    """

    list_display = ["name", "rate_display", "is_default", "created_on"]
    list_filter = ["is_default", "created_on"]
    search_fields = ["name"]
    readonly_fields = ["created_on", "updated_on"]

    fieldsets = (
        (
            "Tax Info",
            {
                "fields": ("name", "rate", "description", "is_default"),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_on", "updated_on"),
            },
        ),
    )

    @admin.display(description="Rate", ordering="rate")
    def rate_display(self, obj):
        """Display rate with percentage symbol."""
        return f"{obj.rate}%"


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    """
    Admin configuration for UnitOfMeasure model.

    Features:
        - Conversion factor display
        - Base unit indicator
    """

    list_display = [
        "name",
        "symbol",
        "conversion_factor",
        "is_base_unit",
        "is_active",
    ]
    list_filter = ["is_base_unit", "is_active"]
    search_fields = ["name", "symbol"]
    readonly_fields = ["created_on", "updated_on"]

    fieldsets = (
        (
            "Unit Info",
            {
                "fields": ("name", "symbol", "description"),
            },
        ),
        (
            "Conversion",
            {
                "fields": ("conversion_factor", "is_base_unit"),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_on", "updated_on"),
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.

    Features:
        - Colored status badge
        - Auto-generated SKU (readonly)
        - Autocomplete for related models
        - Organized fieldsets with collapsible sections
    """

    list_display = [
        "sku",
        "name",
        "product_type",
        "status_badge",
        "category",
        "brand",
        "selling_price",
        "featured",
        "created_on",
    ]
    list_filter = [
        "product_type",
        "status",
        "is_webstore_visible",
        "is_pos_visible",
        "featured",
        "category",
        "brand",
        "created_on",
    ]
    search_fields = [
        "name",
        "sku",
        "barcode",
        "description",
        "short_description",
    ]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["sku", "created_on", "updated_on"]
    autocomplete_fields = ["category", "brand", "tax_class", "unit_of_measure"]
    list_per_page = 25

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "slug",
                    "sku",
                    "barcode",
                    "short_description",
                    "description",
                ),
            },
        ),
        (
            "Classification",
            {
                "fields": ("category", "brand", "product_type", "status"),
            },
        ),
        (
            "Visibility",
            {
                "fields": (
                    "is_webstore_visible",
                    "is_pos_visible",
                    "featured",
                ),
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "cost_price",
                    "selling_price",
                    "mrp",
                    "wholesale_price",
                    "tax_class",
                    "unit_of_measure",
                ),
            },
        ),
        (
            "Physical Attributes",
            {
                "classes": ("collapse",),
                "fields": ("weight", "length", "width", "height"),
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": ("seo_title", "seo_description"),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_on", "updated_on"),
            },
        ),
    )

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        """Display a colored HTML badge based on product status."""
        colors = {
            "draft": "#999",
            "active": "#28a745",
            "archived": "#ffc107",
            "discontinued": "#dc3545",
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    def get_queryset(self, request):
        """Optimize queryset with select_related for list view."""
        return (
            super()
            .get_queryset(request)
            .select_related("category", "brand", "tax_class", "unit_of_measure")
        )
