"""
LankaCommerce Cloud - Production Settings

Strict security settings for production deployment.
All secrets are read from environment variables — nothing is hardcoded.

Required environment variables:
    DJANGO_SECRET_KEY       - Cryptographic signing key
    DJANGO_ALLOWED_HOSTS    - Comma-separated domain list
    DATABASE_URL            - PostgreSQL connection string
    REDIS_URL               - Redis connection string
    SENTRY_DSN              - (optional) Sentry error tracking
"""

import os

from config.settings.base import *  # noqa: F401, F403


# ════════════════════════════════════════════════════════════════════════
# SECURITY  (Task 32)
# ════════════════════════════════════════════════════════════════════════

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# ── HTTPS ──────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── HSTS (HTTP Strict Transport Security) ─────────────────────────────
SECURE_HSTS_SECONDS = 31536000              # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ── Cookies ────────────────────────────────────────────────────────────
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# ── Security headers ──────────────────────────────────────────────────
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# ── CSRF trusted origins ──────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", ""
).split(",")


# ════════════════════════════════════════════════════════════════════════
# DATABASE  (Task 33)
# ════════════════════════════════════════════════════════════════════════
# In production, DATABASE_URL is the canonical source of truth.
# Format: postgres://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
#
# Phase 2 will switch ENGINE to django_tenants.postgresql_backend.

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "lankacommerce"),
        "USER": os.environ.get("DB_USER", "lcc_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "sslmode": os.environ.get("DB_SSLMODE", "require"),
        },
    }
}

# If dj-database-url is installed, uncomment to parse DATABASE_URL:
# import dj_database_url
# DATABASES["default"] = dj_database_url.config(
#     default=os.environ.get("DATABASE_URL"),
#     conn_max_age=60,
#     conn_health_checks=True,
#     ssl_require=True,
# )


# ════════════════════════════════════════════════════════════════════════
# CACHING — Redis  (Task 34)
# ════════════════════════════════════════════════════════════════════════

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 300,                          # 5 minutes
        "KEY_PREFIX": "lcc",
        "VERSION": 1,
        "OPTIONS": {
            # "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# ── Session via cache (faster than database) ──────────────────────────
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ── Celery broker ─────────────────────────────────────────────────────
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)


# ── Channel Layers (Redis-backed) ────────────────────────────────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL", REDIS_URL)],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}


# ════════════════════════════════════════════════════════════════════════
# EMAIL  (Production SMTP)
# ════════════════════════════════════════════════════════════════════════

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@lankacommerce.lk")
EMAIL_SUBJECT_PREFIX = "[LCC] "


# ════════════════════════════════════════════════════════════════════════
# STATIC FILES — WhiteNoise (or Nginx)
# ════════════════════════════════════════════════════════════════════════

# Uncomment when whitenoise is installed:
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Insert "whitenoise.middleware.WhiteNoiseMiddleware" after SecurityMiddleware


# ════════════════════════════════════════════════════════════════════════
# ERROR TRACKING — Sentry (optional)
# ════════════════════════════════════════════════════════════════════════

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    import sentry_sdk  # noqa: E402
    from sentry_sdk.integrations.django import DjangoIntegration  # noqa: E402

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        send_default_pii=False,
    )


# ════════════════════════════════════════════════════════════════════════
# LOGGING
# ════════════════════════════════════════════════════════════════════════

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
