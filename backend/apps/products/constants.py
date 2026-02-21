"""
Products constants module.

Defines choices, status values, and other constants used across
the products application models.
"""

# ════════════════════════════════════════════════════════════════════════
# Product Status Choices
# ════════════════════════════════════════════════════════════════════════

PRODUCT_STATUS_DRAFT = "draft"
PRODUCT_STATUS_ACTIVE = "active"
PRODUCT_STATUS_INACTIVE = "inactive"
PRODUCT_STATUS_DISCONTINUED = "discontinued"

PRODUCT_STATUS_CHOICES = [
    (PRODUCT_STATUS_DRAFT, "Draft"),
    (PRODUCT_STATUS_ACTIVE, "Active"),
    (PRODUCT_STATUS_INACTIVE, "Inactive"),
    (PRODUCT_STATUS_DISCONTINUED, "Discontinued"),
]

# ════════════════════════════════════════════════════════════════════════
# Tax Type Choices (Sri Lankan VAT)
# ════════════════════════════════════════════════════════════════════════

TAX_TYPE_NONE = "none"
TAX_TYPE_STANDARD = "standard"
TAX_TYPE_REDUCED = "reduced"
TAX_TYPE_EXEMPT = "exempt"
TAX_TYPE_ZERO_RATED = "zero_rated"

TAX_TYPE_CHOICES = [
    (TAX_TYPE_NONE, "No Tax"),
    (TAX_TYPE_STANDARD, "Standard Rate"),
    (TAX_TYPE_REDUCED, "Reduced Rate"),
    (TAX_TYPE_EXEMPT, "Tax Exempt"),
    (TAX_TYPE_ZERO_RATED, "Zero Rated"),
]

# Sri Lankan standard VAT rate
SRI_LANKA_VAT_RATE = 18  # percentage

# ════════════════════════════════════════════════════════════════════════
# Variant Attribute Type Choices
# ════════════════════════════════════════════════════════════════════════

VARIANT_ATTR_SIZE = "size"
VARIANT_ATTR_COLOR = "color"
VARIANT_ATTR_MATERIAL = "material"
VARIANT_ATTR_WEIGHT = "weight"
VARIANT_ATTR_CUSTOM = "custom"

VARIANT_ATTRIBUTE_CHOICES = [
    (VARIANT_ATTR_SIZE, "Size"),
    (VARIANT_ATTR_COLOR, "Color"),
    (VARIANT_ATTR_MATERIAL, "Material"),
    (VARIANT_ATTR_WEIGHT, "Weight"),
    (VARIANT_ATTR_CUSTOM, "Custom"),
]
