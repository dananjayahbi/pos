"""Sri Lanka NIC (National Identity Card) validator."""

import re

from django.core.exceptions import ValidationError


# Old format: 9 digits + V or X (e.g., 912345678V)
OLD_NIC_PATTERN = re.compile(r"^(\d{9})[VvXx]$")

# New format: 12 digits (e.g., 199112345678)
NEW_NIC_PATTERN = re.compile(r"^(\d{12})$")


def validate_nic(value):
    """
    Validate Sri Lanka NIC number.

    Supports both old format (9 digits + V/X) and new format (12 digits).

    Old format: YYDDDNNNNV/X
        - YY: Year of birth (2 digits)
        - DDD: Day of year (001-366 male, 501-866 female)
        - NNNN: Sequence number
        - V or X: Suffix

    New format: YYYYDDDNNNNN
        - YYYY: Year of birth (4 digits)
        - DDD: Day of year (001-366 male, 501-866 female)
        - NNNNN: Sequence number
    """
    if not value:
        return

    value = value.strip()

    old_match = OLD_NIC_PATTERN.match(value)
    new_match = NEW_NIC_PATTERN.match(value)

    if not old_match and not new_match:
        raise ValidationError(
            "Invalid NIC format. Use old format (e.g., 912345678V) "
            "or new format (e.g., 199112345678).",
            code="invalid_nic_format",
        )

    if old_match:
        digits = old_match.group(1)
        day_of_year = int(digits[2:5])
    else:
        digits = new_match.group(1)
        day_of_year = int(digits[4:7])

    # Female NICs have 500 added to day of year
    if day_of_year >= 500:
        day_of_year -= 500

    if day_of_year < 1 or day_of_year > 366:
        raise ValidationError(
            "Invalid NIC: day of year out of range.",
            code="invalid_nic_day",
        )


def extract_birth_year_from_nic(nic_value):
    """Extract birth year from NIC number."""
    if not nic_value:
        return None

    nic_value = nic_value.strip()
    old_match = OLD_NIC_PATTERN.match(nic_value)
    new_match = NEW_NIC_PATTERN.match(nic_value)

    if old_match:
        year_part = int(old_match.group(1)[:2])
        return 1900 + year_part
    elif new_match:
        return int(new_match.group(1)[:4])
    return None


def extract_gender_from_nic(nic_value):
    """Extract gender from NIC number (male if day <= 366, female if day > 500)."""
    if not nic_value:
        return None

    nic_value = nic_value.strip()
    old_match = OLD_NIC_PATTERN.match(nic_value)
    new_match = NEW_NIC_PATTERN.match(nic_value)

    if old_match:
        day_of_year = int(old_match.group(1)[2:5])
    elif new_match:
        day_of_year = int(new_match.group(1)[4:7])
    else:
        return None

    return "female" if day_of_year >= 500 else "male"
