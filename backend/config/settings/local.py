"""
LankaCommerce Cloud - Local Development Settings

Extends base settings with development-specific overrides:
    - DEBUG enabled with detailed error pages
    - PostgreSQL database (Docker or remote)
    - Console email backend
    - Debug toolbar + django-extensions

Usage:
    Set DJANGO_ENV=local (default) or run without setting it.
"""

import os

from config.settings.base import *  # noqa: F401, F403


# ════════════════════════════════════════════════════════════════════════
# DEBUG SETTINGS  (Task 29)
# ════════════════════════════════════════════════════════════════════════

DEBUG = True

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-dev-key-do-not-use-in-production",
)

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0",
).split(",")

# Required for django-debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "10.0.2.2",  # Docker host (common)
]

# ── Development apps ──────────────────────────────────────────────────
INSTALLED_APPS += [  # noqa: F405
    # "debug_toolbar",          # Uncomment after pip install django-debug-toolbar
    # "django_extensions",      # Uncomment after pip install django-extensions
]

# ── Development middleware ─────────────────────────────────────────────
MIDDLEWARE += [  # noqa: F405
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # Uncomment with debug_toolbar
]


# ════════════════════════════════════════════════════════════════════════
# DATABASE  (Task 30)
# ════════════════════════════════════════════════════════════════════════
# Connects to PostgreSQL. Reads credentials from environment variables
# with sensible defaults for local Docker development.
#
# In Phase 2 the ENGINE will change to django_tenants.postgresql_backend.

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "llc-dev"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "connect_timeout": 5,
        },
    }
}


# ════════════════════════════════════════════════════════════════════════
# EMAIL  (Task 31)
# ════════════════════════════════════════════════════════════════════════
# Console backend prints emails to terminal — simplest for development.
# Switch to MailHog (Docker) for full SMTP testing if needed.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "noreply@localhost"

EMAIL_SUBJECT_PREFIX = "[LCC Dev] "

# ── MailHog alternative (uncomment to use MailHog in Docker) ──────────
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "mailhog"
# EMAIL_PORT = 1025
