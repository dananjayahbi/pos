"""Sri Lanka phone number validator."""

import re

from django.core.exceptions import ValidationError


# +94 followed by 9 digits, or 0 followed by 9 digits
SL_PHONE_PATTERN = re.compile(r"^(\+94|0)\d{9}$")


def validate_sl_phone(value):
    """
    Validate Sri Lanka phone number format.

    Accepts: +94XXXXXXXXX or 0XXXXXXXXX (10-12 chars total).
    """
    if not value:
        return

    cleaned = re.sub(r"[\s\-()]", "", value)

    if not SL_PHONE_PATTERN.match(cleaned):
        raise ValidationError(
            "Invalid phone number format. Use +94XXXXXXXXX or 0XXXXXXXXX.",
            code="invalid_phone_format",
        )
