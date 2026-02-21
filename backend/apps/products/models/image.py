"""
ProductImage model for the products application.

Defines the ProductImage model which allows multiple images
per product. Each image has a sort order and one image per
product can be designated as the primary image.
"""

from django.db import models

from apps.core.mixins import UUIDMixin, TimestampMixin


def product_image_upload_path(instance, filename):
    """Generate upload path for product images."""
    return f"products/{instance.product_id}/images/{filename}"


class ProductImage(UUIDMixin, TimestampMixin, models.Model):
    """
    Product image model supporting multiple images per product.

    Each product can have multiple images with a sort order.
    One image per product should be marked as the primary image
    for display on listing pages.

    Fields:
        product: FK to Product model.
        image: The image file.
        alt_text: Alternative text for accessibility.
        is_primary: Whether this is the main product image.
        sort_order: Controls display order of images.
    """

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Product",
        help_text="The product this image belongs to.",
    )
    image = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name="Image",
        help_text="Product image file.",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Alt Text",
        help_text="Alternative text for accessibility.",
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Primary Image",
        help_text="Whether this is the main product image.",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sort Order",
        help_text="Controls display order. Lower values appear first.",
    )

    class Meta:
        app_label = "products"
        db_table = "products_productimage"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["sort_order"]
        indexes = [
            models.Index(
                fields=["product", "is_primary"],
                name="idx_prodimg_product_primary",
            ),
        ]

    def __str__(self):
        """Return image description."""
        primary = " (primary)" if self.is_primary else ""
        return f"Image for {self.product_id}{primary}"
