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

from config.env import BASE_DIR, env  # Centralized env loader


# ── Future imports (uncomment when packages are installed) ──────────────
# import dj_database_url                        # database URL parsing


# ════════════════════════════════════════════════════════════════════════
# PATH CONFIGURATION
# ════════════════════════════════════════════════════════════════════════
# BASE_DIR is imported from config.env and points to backend/


# ════════════════════════════════════════════════════════════════════════
# SECURITY — SECRET KEY / DEBUG / HOSTS
# ════════════════════════════════════════════════════════════════════════
# These use the centralized env loader from config.env.
# Defaults are defined there; override via .env or system env vars.

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS")


# ════════════════════════════════════════════════════════════════════════
# APPLICATION DEFINITION  (Task 20)
# ════════════════════════════════════════════════════════════════════════
# NOTE: INSTALLED_APPS is now defined in database.py using the
# django-tenants pattern: SHARED_APPS + unique TENANT_APPS.
#
# The lists below are kept as reference for which apps are installed,
# but they are NO LONGER used to build INSTALLED_APPS. Any new app
# must be added to SHARED_APPS or TENANT_APPS in database.py.
#
# See: backend/config/settings/database.py

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS: list[str] = [
    "django_tenants",                    # Multi-tenancy (Phase 2)
    "channels",                          # Django Channels (WebSocket)
    "rest_framework",                    # Django REST Framework
    "django_filters",                    # Query filtering
    "rest_framework_simplejwt",          # JWT authentication
    "drf_spectacular",                   # OpenAPI documentation
    "corsheaders",                       # CORS handling
    "django_celery_beat",                # Periodic task scheduling
    "django_celery_results",             # Task result storage
]

LOCAL_APPS: list[str] = [
    # Core Framework
    "apps.core",                         # Core utilities (Phase 3)
    "apps.tenants",                      # Tenant models (Phase 2)
    "apps.users",                        # User management (Phase 3)

    # Business Modules - Phase 4
    "apps.products",                     # Product catalog
    "apps.inventory",                    # Stock & warehouse
    "apps.vendors",                      # Supplier management

    # Business Modules - Phase 5
    "apps.sales",                        # Orders, invoicing, POS
    "apps.customers",                    # Customer CRM

    # Advanced Modules - Phase 6
    "apps.hr",                           # Human resources
    "apps.accounting",                   # Accounting & finance
    "apps.reports",                      # Reports & analytics

    # Platform Apps
    "apps.webstore",                     # E-commerce storefront
    "apps.integrations",                 # Third-party integrations
]

# INSTALLED_APPS is defined in database.py via SHARED_APPS + TENANT_APPS.
# The import happens via: from config.settings.database import *


# ════════════════════════════════════════════════════════════════════════
# MIDDLEWARE  (Task 21)
# ════════════════════════════════════════════════════════════════════════
# Order is critical — security first, then session, auth, etc.

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "django_tenants.middleware.main.TenantMainMiddleware",   # Phase 2
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middleware will be added here (Phase 3)
    # "apps.platform.middleware.feature_flags.FeatureFlagMiddleware",  # Phase 3
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
# DJANGO REST FRAMEWORK  (Task 36)
# ════════════════════════════════════════════════════════════════════════

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
}


# ════════════════════════════════════════════════════════════════════════
# CORS  (Task 39)
# ════════════════════════════════════════════════════════════════════════
# Defaults: restrictive.  local.py opens up for development.

CORS_ALLOW_ALL_ORIGINS = False  # Overridden in local.py
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")
CORS_ALLOWED_ORIGINS: list[str] = env.list("CORS_ALLOWED_ORIGINS")


# ════════════════════════════════════════════════════════════════════════
# SIMPLE JWT  (Task 42)
# ════════════════════════════════════════════════════════════════════════

from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME_MINUTES"),
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env.int("JWT_REFRESH_TOKEN_LIFETIME_DAYS"),
    ),
    "ROTATE_REFRESH_TOKENS": env.bool("JWT_ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": env.bool("JWT_BLACKLIST_AFTER_ROTATION"),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}


# ════════════════════════════════════════════════════════════════════════
# DRF SPECTACULAR — OpenAPI 3.0  (Task 43)
# ════════════════════════════════════════════════════════════════════════

SPECTACULAR_SETTINGS = {
    "TITLE": "LankaCommerce Cloud API",
    "DESCRIPTION": "Multi-tenant ERP, POS & E-commerce REST API for Sri Lanka",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}


# ════════════════════════════════════════════════════════════════════════
# CELERY  (Tasks 44-46)
# ════════════════════════════════════════════════════════════════════════

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = env("TIME_ZONE")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# ════════════════════════════════════════════════════════════════════════
# CHANNEL LAYERS  (Task 70)
# ════════════════════════════════════════════════════════════════════════
# Redis-backed channel layer for WebSocket message routing.
# Each environment file may override with different backends.
# Redis database allocation: 0=Celery, 1=Cache, 2=Channels, 15=Testing

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL")],
        },
    },
}


# ════════════════════════════════════════════════════════════════════════
# DATABASE  (Task 23 — Configured in Phase 2)
# ════════════════════════════════════════════════════════════════════════
# Database credentials are NEVER stored here.
# Each environment file (local.py, production.py, test.py) overrides
# DATABASES with its own connection configuration.
#
# Multi-tenancy settings (TENANT_MODEL, TENANT_DOMAIN_MODEL,
# DATABASE_ROUTERS) are centralized in config/settings/database.py.

from config.settings.database import *  # noqa: E402, F401, F403

DATABASES: dict = {}


# ════════════════════════════════════════════════════════════════════════
# AUTHENTICATION  (Task 24)
# ════════════════════════════════════════════════════════════════════════

# Custom user model — must be set before first migration.
# PlatformUser is the platform-level auth model in the public schema.
# Tenant-scoped users will be handled separately in the users app.
AUTH_USER_MODEL = "platform.PlatformUser"

# TENANT_MODEL and TENANT_DOMAIN_MODEL are imported from
# config/settings/database.py via the wildcard import above.

# Authentication backends — will be extended for JWT, social auth.
# EmailBackend enables authentication using email + password, which
# aligns with PlatformUser's USERNAME_FIELD = "email".
AUTHENTICATION_BACKENDS = [
    "apps.platform.backends.EmailBackend",
]

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

# WhiteNoise: Serve static files with compression and caching
# Media storage: Tenant-aware partitioning (each tenant gets MEDIA_ROOT/<schema_name>/)
STORAGES = {
    "default": {
        "BACKEND": "django_tenants.files.storage.TenantFileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


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
