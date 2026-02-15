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

import os  # noqa: F401

from config.env import env  # noqa: F401
from config.settings.base import *  # noqa: F401, F403


# ════════════════════════════════════════════════════════════════════════
# SECURITY  (Task 32)
# ════════════════════════════════════════════════════════════════════════

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

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
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=[],
)


# ════════════════════════════════════════════════════════════════════════
# DATABASE  (Task 33)
# ════════════════════════════════════════════════════════════════════════
# In production, DATABASE_URL is the canonical source of truth.
# Format: postgres://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
#
# Phase 2 will switch ENGINE to django_tenants.postgresql_backend.

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("DB_NAME", default="lankacommerce"),
        "USER": env("DB_USER", default="lcc_user"),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env.int("DB_PORT", default=5432),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "sslmode": env("DB_SSLMODE", default="require"),
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

REDIS_URL = env("REDIS_URL")

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
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")


# ── Channel Layers (Redis-backed) ────────────────────────────────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL")],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}


# ════════════════════════════════════════════════════════════════════════
# EMAIL  (Production SMTP)
# ════════════════════════════════════════════════════════════════════════

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@lankacommerce.lk")
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

SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk  # noqa: E402
    from sentry_sdk.integrations.django import DjangoIntegration  # noqa: E402

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.1),
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
