"""
DRF Serializers for the products app.

Provides serializers for categories, brands, tax classes,
units of measure, and products with different strategies:
- List serializers: Lightweight for list views
- Detail serializers: Complete info with nested relations
- Create/Update serializers: Validation and business logic
- Tree serializers: Recursive nested structures (categories)
"""

from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from apps.products.models import Brand, Category, Product, TaxClass, UnitOfMeasure
from apps.products.constants import PRODUCT_TYPES, PRODUCT_STATUS


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for category list views.

    Minimal fields optimised for large result sets.
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "parent",
            "is_active",
            "display_order",
            "level",
        ]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    """
    Base serializer for Category with common fields.

    Includes parent name for context and children count.
    """

    parent_name = serializers.CharField(
        source="parent.name", read_only=True, default=None
    )
    children_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "parent_name",
            "description",
            "image",
            "icon",
            "is_active",
            "display_order",
            "children_count",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "created_on", "updated_on"]


class CategoryDetailSerializer(CategorySerializer):
    """
    Detailed serializer including SEO fields and tree info.

    Used for single-category retrieval (GET /categories/{id}/).
    """

    is_root = serializers.BooleanField(read_only=True)
    is_leaf = serializers.BooleanField(read_only=True)
    descendants_count = serializers.IntegerField(read_only=True)
    full_path = serializers.SerializerMethodField()
    children = CategoryListSerializer(many=True, read_only=True, source="get_children")

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + [
            "seo_title",
            "seo_description",
            "seo_keywords",
            "is_root",
            "is_leaf",
            "descendants_count",
            "full_path",
            "children",
        ]

    def get_full_path(self, obj) -> str:
        """Return breadcrumb path string."""
        return obj.get_full_path()


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Recursive serializer for the full category tree.

    Each node carries its nested children down to leaf level.
    Used by the ``/categories/tree/`` endpoint.
    """

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "is_active",
            "display_order",
            "level",
            "children",
        ]

    def get_children(self, obj) -> list:
        """Recursively serialize active children."""
        children_qs = obj.get_children().filter(is_active=True)
        return CategoryTreeSerializer(children_qs, many=True).data


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating categories.

    Handles slug auto-generation and parent validation.
    """

    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "parent",
            "description",
            "image",
            "icon",
            "is_active",
            "display_order",
            "seo_title",
            "seo_description",
            "seo_keywords",
        ]
        extra_kwargs = {
            "slug": {"required": False, "allow_blank": True},
        }

    # ── Validation ──────────────────────────────────────────────────

    def validate_parent(self, value):
        """Prevent a category from being set as its own parent."""
        if value and self.instance and value.pk == self.instance.pk:
            raise serializers.ValidationError(
                "A category cannot be its own parent."
            )
        # Prevent moving a category under one of its descendants
        if (
            value
            and self.instance
            and self.instance.is_ancestor_of(value)
        ):
            raise serializers.ValidationError(
                "Cannot move a category under its own descendant."
            )
        return value

    def validate_name(self, value):
        """Ensure name is not empty after stripping."""
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Category name cannot be blank.")
        return stripped

    # ── Slug auto-generation ────────────────────────────────────────

    def _generate_unique_slug(self, name):
        """Generate a unique slug within the tenant schema."""
        base_slug = slugify(name)
        if not base_slug:
            base_slug = "category"
        slug = base_slug
        counter = 1
        qs = Category.objects.all()
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        while qs.filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"
        return slug

    def create(self, validated_data):
        """Create category, auto-generating slug when missing."""
        if not validated_data.get("slug"):
            validated_data["slug"] = self._generate_unique_slug(
                validated_data["name"]
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update category, regenerating slug if name changed and slug blank."""
        if not validated_data.get("slug") and "name" in validated_data:
            if validated_data["name"] != instance.name:
                validated_data["slug"] = self._generate_unique_slug(
                    validated_data["name"]
                )
        return super().update(instance, validated_data)


# ════════════════════════════════════════════════════════════════════════
# Brand Serializer
# ════════════════════════════════════════════════════════════════════════


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand model.

    Used for list, detail, create, and update operations.
    """

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "website",
            "is_active",
        ]
        read_only_fields = ["id", "slug"]


# ════════════════════════════════════════════════════════════════════════
# TaxClass Serializer
# ════════════════════════════════════════════════════════════════════════


class TaxClassSerializer(serializers.ModelSerializer):
    """
    Serializer for TaxClass model.

    Used for list, detail, create, and update operations.
    """

    class Meta:
        model = TaxClass
        fields = [
            "id",
            "name",
            "rate",
            "description",
            "is_default",
            "is_active",
        ]
        read_only_fields = ["id"]


# ════════════════════════════════════════════════════════════════════════
# UnitOfMeasure Serializer
# ════════════════════════════════════════════════════════════════════════


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    """
    Serializer for UnitOfMeasure model.

    Used for list, detail, create, and update operations.
    """

    class Meta:
        model = UnitOfMeasure
        fields = [
            "id",
            "name",
            "symbol",
            "description",
            "conversion_factor",
            "is_base_unit",
            "is_active",
        ]
        read_only_fields = ["id"]


# ════════════════════════════════════════════════════════════════════════
# Product Serializers
# ════════════════════════════════════════════════════════════════════════


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product list views.

    Includes source-based fields for category/brand names and
    display values for choices fields.
    """

    category_name = serializers.CharField(
        source="category.name", read_only=True
    )
    brand_name = serializers.CharField(
        source="brand.name", read_only=True, allow_null=True
    )
    product_type_display = serializers.CharField(
        source="get_product_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "barcode",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "product_type",
            "product_type_display",
            "status",
            "status_display",
            "cost_price",
            "selling_price",
            "is_webstore_visible",
            "is_pos_visible",
            "featured",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "slug", "created_on", "updated_on"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for single product retrieval.

    Includes nested related objects and all product fields.
    """

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True, allow_null=True)
    tax_class = TaxClassSerializer(read_only=True, allow_null=True)
    unit_of_measure = UnitOfMeasureSerializer(read_only=True, allow_null=True)
    product_type_display = serializers.CharField(
        source="get_product_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "barcode",
            "description",
            "short_description",
            "category",
            "brand",
            "product_type",
            "product_type_display",
            "status",
            "status_display",
            "is_webstore_visible",
            "is_pos_visible",
            "featured",
            "tax_class",
            "unit_of_measure",
            "cost_price",
            "selling_price",
            "mrp",
            "wholesale_price",
            "weight",
            "length",
            "width",
            "height",
            "seo_title",
            "seo_description",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["id", "slug", "created_on", "updated_on"]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating products.

    Handles SKU auto-generation, slug generation, and uniqueness validation.
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "sku",
            "barcode",
            "description",
            "short_description",
            "category",
            "brand",
            "product_type",
            "status",
            "is_webstore_visible",
            "is_pos_visible",
            "featured",
            "tax_class",
            "unit_of_measure",
            "cost_price",
            "selling_price",
            "mrp",
            "wholesale_price",
            "weight",
            "length",
            "width",
            "height",
            "seo_title",
            "seo_description",
        ]
        extra_kwargs = {
            "sku": {"required": False, "allow_blank": True},
            "slug": {"required": False, "allow_blank": True},
            "brand": {"required": False, "allow_null": True},
            "barcode": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
        }

    # ── Validation ──────────────────────────────────────────────────

    def validate_sku(self, value):
        """Ensure SKU is unique (exclude current instance on update)."""
        if not value:
            return value
        qs = Product.objects.filter(sku=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A product with this SKU already exists."
            )
        return value

    def validate_barcode(self, value):
        """Ensure barcode is unique (exclude current instance on update)."""
        if not value:
            return value
        qs = Product.objects.filter(barcode=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A product with this barcode already exists."
            )
        return value

    # ── SKU Generation ──────────────────────────────────────────────

    def _generate_sku(self, category):
        """
        Auto-generate a unique SKU based on category.

        Format: PRD-{CATEGORY_CODE}-{NUMBER:05d}
        where CATEGORY_CODE is the first 4 chars of the category slug
        uppercased, and NUMBER is an auto-incrementing counter.
        """
        category_code = category.slug[:4].upper() if category.slug else "GNRL"
        prefix = f"PRD-{category_code}-"
        last_product = (
            Product.objects.filter(sku__startswith=prefix)
            .order_by("-sku")
            .first()
        )
        if last_product:
            try:
                last_number = int(last_product.sku.split("-")[-1])
                next_number = last_number + 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        return f"{prefix}{next_number:05d}"

    # ── Slug Generation ─────────────────────────────────────────────

    def _generate_unique_slug(self, name):
        """Generate a unique slug for the product."""
        base_slug = slugify(name)
        if not base_slug:
            base_slug = "product"
        slug = base_slug
        counter = 1
        qs = Product.objects.all()
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        while qs.filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"
        return slug

    # ── Create / Update ─────────────────────────────────────────────

    @transaction.atomic
    def create(self, validated_data):
        """Create product with auto-generated SKU and slug if blank."""
        if not validated_data.get("sku"):
            validated_data["sku"] = self._generate_sku(
                validated_data["category"]
            )
        if not validated_data.get("slug"):
            validated_data["slug"] = self._generate_unique_slug(
                validated_data["name"]
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update product, regenerating slug if name changed and slug blank."""
        if not validated_data.get("slug") and "name" in validated_data:
            if validated_data["name"] != instance.name:
                validated_data["slug"] = self._generate_unique_slug(
                    validated_data["name"]
                )
        return super().update(instance, validated_data)
