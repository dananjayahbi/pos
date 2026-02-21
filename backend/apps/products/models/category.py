"""
Category model for the products application.

Defines the Category model which supports hierarchical product
categorization using a self-referential foreign key pattern.
Categories are tenant-specific — each tenant has its own
independent category tree.
"""

from django.db import models
from django.utils.text import slugify

from apps.core.mixins import UUIDMixin, TimestampMixin


def category_image_upload_path(instance, filename):
    """Generate upload path for category images."""
    return f"categories/{instance.slug}/{filename}"


class Category(UUIDMixin, TimestampMixin, models.Model):
    """
    Product category with hierarchical support.

    Supports a tree structure via the self-referential parent field.
    Root categories have parent=None. Each category has a unique
    slug within its tenant schema for URL-friendly identification.

    Fields:
        name: Display name of the category (max 255 chars).
        slug: URL-friendly identifier, unique per tenant schema.
        parent: Self-referential FK for category hierarchy.
            Null for root categories.
        image: Optional category image for branding/display.
        is_active: Controls category visibility. Inactive categories
            and their products are hidden from the storefront but
            remain accessible in the admin.
        description: Optional description for the category.
        sort_order: Integer for controlling display order.
    """

    # ── Core Fields ─────────────────────────────────────────────────
    name = models.CharField(
        max_length=255,
        verbose_name="Category Name",
        help_text="Display name of the category.",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug",
        help_text="URL-friendly identifier. Unique per tenant.",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Description",
        help_text="Optional description for the category.",
    )

    # ── Hierarchy ───────────────────────────────────────────────────
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Category",
        help_text="Parent category. Null for root categories.",
    )

    # ── Branding ────────────────────────────────────────────────────
    image = models.ImageField(
        upload_to=category_image_upload_path,
        null=True,
        blank=True,
        verbose_name="Category Image",
        help_text="Optional image for category branding.",
    )

    # ── Visibility & Ordering ───────────────────────────────────────
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active",
        help_text="Controls category visibility on the storefront.",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sort Order",
        help_text="Controls display order. Lower values appear first.",
    )

    class Meta:
        app_label = "products"
        db_table = "products_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(
                fields=["is_active", "sort_order"],
                name="idx_category_active_sort",
            ),
            models.Index(
                fields=["parent"],
                name="idx_category_parent",
            ),
        ]

    def __str__(self):
        """Return the full category path (e.g., 'Electronics > Phones')."""
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_root(self):
        """Return True if this is a root category (no parent)."""
        return self.parent_id is None

    @property
    def depth(self):
        """Return the depth of this category in the tree (0 for root)."""
        level = 0
        current = self
        while current.parent_id is not None:
            level += 1
            current = current.parent
        return level
