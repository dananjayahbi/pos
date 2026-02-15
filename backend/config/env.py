"""
LankaCommerce Cloud - Environment Configuration

Centralized environment variable loading and parsing for all Django settings.
This module provides a single `env` reader instance that all settings files
should use instead of directly accessing os.environ.

Loading Order:
    1. System environment variables (highest priority)
    2. .env file in backend/ directory (if present)
    3. Default values defined in this module (lowest priority)

Usage in settings files:
    from config.env import env, BASE_DIR

    SECRET_KEY = env("DJANGO_SECRET_KEY")
    DEBUG = env.bool("DEBUG")
"""

from pathlib import Path

import environ

# ════════════════════════════════════════════════════════════════════════
# BASE DIRECTORY
# ════════════════════════════════════════════════════════════════════════
# env.py  → config/
# .parent → backend/   ← this is BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent

# ════════════════════════════════════════════════════════════════════════
# ENVIRONMENT READER
# ════════════════════════════════════════════════════════════════════════
# Define the default schema for environment variables.
# These defaults are used when a variable is not set in the environment
# or in the .env file. For secrets, defaults should be clearly unsafe
# so that they are never accidentally used in production.

env = environ.Env(
    # ── Security ────────────────────────────────────────────────────────
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "django-insecure-CHANGE-ME-IN-ENVIRONMENT-SETTINGS"),
    ALLOWED_HOSTS=(list, []),

    # ── Database ────────────────────────────────────────────────────────
    DATABASE_URL=(str, "postgres://postgres:postgres@localhost:5432/lankacommerce"),

    # ── Redis / Cache ───────────────────────────────────────────────────
    REDIS_URL=(str, "redis://localhost:6379/0"),
    CACHE_URL=(str, "redis://localhost:6379/1"),

    # ── Celery ──────────────────────────────────────────────────────────
    CELERY_BROKER_URL=(str, "redis://localhost:6379/0"),
    CELERY_RESULT_BACKEND=(str, "redis://localhost:6379/0"),

    # ── Email ───────────────────────────────────────────────────────────
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),

    # ── Localization ────────────────────────────────────────────────────
    LANGUAGE_CODE=(str, "en-us"),
    TIME_ZONE=(str, "Asia/Colombo"),

    # ── Application ─────────────────────────────────────────────────────
    DJANGO_SETTINGS_MODULE=(str, "config.settings.local"),
    LOG_LEVEL=(str, "INFO"),
)

# ════════════════════════════════════════════════════════════════════════
# ENVIRONMENT FILE LOADING
# ════════════════════════════════════════════════════════════════════════
# Loading order (last wins):
#   1. Default values defined above (lowest priority)
#   2. .env file in the backend/ directory
#   3. System environment variables (highest priority)
#
# The .env file is optional. In production, environment variables should
# be set directly in the deployment environment (Docker, systemd, etc.).
# The .env file is primarily for local development convenience.

ENV_FILE = BASE_DIR / ".env"
ENV_FILE_LOCAL = BASE_DIR / ".env.local"

# Read .env.local first (if present), then .env on top (if present).
# This allows .env to override .env.local values when both exist.
if ENV_FILE_LOCAL.is_file():
    env.read_env(str(ENV_FILE_LOCAL))

if ENV_FILE.is_file():
    env.read_env(str(ENV_FILE))


# ════════════════════════════════════════════════════════════════════════
# CASTING HELPERS
# ════════════════════════════════════════════════════════════════════════
# django-environ provides built-in casting via the Env class:
#
#   env("VAR")              → str
#   env.bool("VAR")         → bool
#   env.int("VAR")          → int
#   env.float("VAR")        → float
#   env.list("VAR")         → list[str]
#   env.tuple("VAR")        → tuple
#   env.dict("VAR")         → dict
#   env.url("VAR")          → urllib.parse.ParseResult
#   env.db_url("VAR")       → dict (Django DATABASES format)
#   env.cache_url("VAR")    → dict (Django CACHES format)
#   env.path("VAR")         → environ.Path
#
# These are available directly on the `env` instance imported from
# this module. No additional helpers are needed.
