"""
LankaCommerce Cloud - Base Settings

Core Django settings shared across all environments (local, production, test).
Environment-specific overrides are in their respective files:
    - local.py      → Development
    - production.py → Production
    - test.py       → Testing

Generated initially by 'django-admin startproject' using Django 5.2.11,
then restructured into a modular settings package.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os  # noqa: F401
from pathlib import Path

# ── Future imports (uncomment when packages are installed) ──────────────
# from decouple import config, Csv              # environment variables
# import dj_database_url                        # database URL parsing


# ════════════════════════════════════════════════════════════════════════
# PATH CONFIGURATION
# ════════════════════════════════════════════════════════════════════════
# __file__  → base.py
# .parent   → config/settings/
# .parent   → config/
# .parent   → backend/   ← this is BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ════════════════════════════════════════════════════════════════════════
# SECURITY — SECRET KEY / DEBUG / HOSTS
# ════════════════════════════════════════════════════════════════════════
# These are placeholders; they will be overridden by environment-specific
# settings files. NEVER deploy with these values.

SECRET_KEY = "django-insecure-CHANGE-ME-IN-ENVIRONMENT-SETTINGS"

DEBUG = False  # Overridden in local.py / test.py

ALLOWED_HOSTS: list[str] = []  # Overridden per environment


# ════════════════════════════════════════════════════════════════════════
# APPLICATION DEFINITION  (Task 20)
# ════════════════════════════════════════════════════════════════════════

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS: list[str] = [
    # "django_tenants",                  # Multi-tenancy (Phase 2)
    # "rest_framework",                  # Django REST Framework (Group D)
    # "corsheaders",                     # CORS handling (Group D)
    # "django_filters",                  # Filtering (Group D)
]

LOCAL_APPS: list[str] = [
    # "apps.core",                       # Core utilities (Phase 3)
    # "apps.users",                      # User management (Phase 3)
    # "apps.tenants",                    # Tenant models (Phase 2)
    # "apps.inventory",                  # Inventory module (Phase 4)
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ════════════════════════════════════════════════════════════════════════
# MIDDLEWARE  (Task 21)
# ════════════════════════════════════════════════════════════════════════
# Order is critical — security first, then session, auth, etc.

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "django_tenants.middleware.main.TenantMainMiddleware",   # Phase 2
    # "corsheaders.middleware.CorsMiddleware",                 # Group D
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware will be added here (Phase 3)
]


# ════════════════════════════════════════════════════════════════════════
# URL CONFIGURATION
# ════════════════════════════════════════════════════════════════════════

ROOT_URLCONF = "config.urls"


# ════════════════════════════════════════════════════════════════════════
# TEMPLATES  (Task 22)
# ════════════════════════════════════════════════════════════════════════

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ════════════════════════════════════════════════════════════════════════
# WSGI / ASGI
# ════════════════════════════════════════════════════════════════════════

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# ════════════════════════════════════════════════════════════════════════
# DATABASE  (Task 23 — Placeholder)
# ════════════════════════════════════════════════════════════════════════
# Database credentials are NEVER stored here.
# Each environment file (local.py, production.py, test.py) overrides
# DATABASES with its own configuration.
#
# Expected format for PostgreSQL with django-tenants (Phase 2):
#   DATABASES = {
#       "default": {
#           "ENGINE": "django_tenants.postgresql_backend",
#           "NAME": ...,
#           "USER": ...,
#           "PASSWORD": ...,
#           "HOST": ...,
#           "PORT": "5432",
#       }
#   }

DATABASES: dict = {}


# ════════════════════════════════════════════════════════════════════════
# AUTHENTICATION  (Task 24)
# ════════════════════════════════════════════════════════════════════════

# Custom user model — will be set in Phase 3 when users app is created
# AUTH_USER_MODEL = "users.User"

# Authentication backends — will be extended for JWT, social auth
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ════════════════════════════════════════════════════════════════════════
# INTERNATIONALIZATION & LOCALIZATION  (Task 25)
# ════════════════════════════════════════════════════════════════════════
# Sri Lanka-first: Asia/Colombo (UTC+5:30), English primary, Sinhala & Tamil

LANGUAGE_CODE = "en"

TIME_ZONE = "Asia/Colombo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Supported languages: English (primary), Sinhala, Tamil
LANGUAGES = [
    ("en", "English"),
    ("si", "Sinhala"),
    ("ta", "Tamil"),
]

# Translation file location
LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ════════════════════════════════════════════════════════════════════════
# STATIC FILES  (Task 26)
# ════════════════════════════════════════════════════════════════════════

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# ════════════════════════════════════════════════════════════════════════
# MEDIA FILES  (Task 27)
# ════════════════════════════════════════════════════════════════════════
# User-uploaded content (product images, documents, avatars, logos).
# Development: local filesystem.  Production: S3/cloud (overridden).

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# Upload size limits (10 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024    # 10 MB


# ════════════════════════════════════════════════════════════════════════
# SECURITY DEFAULTS  (Task 28)
# ════════════════════════════════════════════════════════════════════════
# Conservative defaults for base.  local.py relaxes; production.py hardens.

# ── CSRF ───────────────────────────────────────────────────────────────
CSRF_COOKIE_SECURE = False           # True in production
CSRF_COOKIE_HTTPONLY = False          # True in production
CSRF_TRUSTED_ORIGINS: list[str] = [] # Overridden per environment

# ── Session ────────────────────────────────────────────────────────────
SESSION_COOKIE_SECURE = False        # True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600         # 2 weeks (seconds)

# ── Security Headers ──────────────────────────────────────────────────
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ── HTTPS / HSTS (disabled in base; enabled in production.py) ─────────
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False


# ════════════════════════════════════════════════════════════════════════
# DEFAULT PRIMARY KEY
# ════════════════════════════════════════════════════════════════════════

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
