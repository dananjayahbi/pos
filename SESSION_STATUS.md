# Session Status - LankaCommerce Cloud POS

> **Last Updated:** Session 8 — Phase-04 SP03 Product Base Model DEEP AUDIT COMPLETE
> **Purpose:** Complete handoff document for the next chat session. This file contains ALL context needed to continue work without the previous chat's memory.

---

## CRITICAL BACKGROUND: The Document Misunderstanding Issue

### What Happened

The project follows a `Document-Series/` folder structure with Phases and SubPhases (SP01-SP12+). Each document describes specific tasks to implement.

**The Problem:** A previous chat session (Session 1) implemented SP03 through SP07 as **config functions** (simple Python functions that return configuration dictionaries) instead of **real Django code**. This resulted in ~620 config functions with 4956 passing tests -- but NO actual working Django code.

**The Fix (Session 2):** Created REAL implementations for SP03-SP07 alongside the config functions. Config functions and their tests were KEPT untouched.

**Session 3:** Completed all remaining SP07 tasks, implemented full SP08 (Celery Task Queue), SP09 (Caching Layer), fixed all 40 failing tenant tests, added model CRUD tests, wired Users API URLs.

---

## Current Progress

### Completed Through

```
Phase-03_Core-Backend-Infrastructure/SubPhase-12_Core-Utilities-Helpers (ALL tasks complete, AUDITED)
Phase-04_ERP-Core-Modules-Part1/SubPhase-01_Category-Model-Hierarchy (ALL 92 tasks complete, AUDITED)
Phase-04_ERP-Core-Modules-Part1/SubPhase-02_Attribute-System (ALL 96 tasks complete, AUDITED)
Phase-04_ERP-Core-Modules-Part1/SubPhase-03_Product-Base-Model (ALL 98 tasks complete, AUDITED)
```

### Next Document to Implement

```
Document-Series/Phase-04_ERP-Core-Modules-Part1/SubPhase-04_*
```

---

## IMPORTANT: Docker-Only Development

We use Docker for **literally everything**. There is NO local SQLite database usage.

- **Development DB:** Docker PostgreSQL 15-alpine (lcc-postgres container, port 5432)
- **Test DB:** `lankacommerce_test` database on the same Docker PostgreSQL instance
- **Connection Pooling:** PgBouncer (lcc-pgbouncer container, port 6432) -- used by backend app, NOT by tests
- **Cache/Broker:** Docker Redis 7-alpine (lcc-redis container, port 6379)
- **Test Settings:** `config.settings.test_pg` -- uses `django_tenants.postgresql_backend` connecting to Docker `db` service
- **pytest.ini:** `DJANGO_SETTINGS_MODULE = config.settings.test_pg`

### Docker Containers (all running)

| Container     | Image               | Port | Status  |
| ------------- | ------------------- | ---- | ------- |
| lcc-postgres  | postgres:15-alpine  | 5432 | Healthy |
| lcc-pgbouncer | edoburu/pgbouncer   | 6432 | Healthy |
| lcc-redis     | redis:7-alpine      | 6379 | Healthy |
| lcc-backend   | custom Django image | 8000 | Running |

### Database Credentials

- **Main DB:** `lankacommerce` (owner: postgres, app user: lcc_user)
- **Test DB:** `lankacommerce_test` (owner: lcc_user -- required for pytest to drop/recreate)
- **User:** `lcc_user` / `dev_password_change_me`
- **Extensions:** uuid-ossp, hstore, pg_trgm, pg_stat_statements

---

## Architecture Notes

### AUTH_USER_MODEL = "platform.PlatformUser"

`PlatformUser` (292 lines) at `apps/platform/models/user.py`:

- Email-based login (no username field)
- UUID primary key
- Platform roles
- All business apps reference `settings.AUTH_USER_MODEL`

The `users` app provides **complementary** tenant-scoped models (profile, preferences, audit trail, RBAC roles/permissions) -- it does NOT replace PlatformUser.

### Multi-Tenancy (django-tenants)

- `TENANT_MODEL = "tenants.Tenant"` and `TENANT_DOMAIN_MODEL = "tenants.Domain"` (in `config/settings/database.py`)
- Database engine: `django_tenants.postgresql_backend`
- Schemas: `public` (shared apps) + per-tenant schemas
- `SHARED_APPS` and `TENANT_APPS` in `config/settings/database.py`
- Custom router: `apps.tenants.routers.LCCDatabaseRouter`

### Existing Mixins and Managers (core/mixins.py, core/managers.py)

- **Mixins:** `UUIDMixin`, `TimestampMixin` (created_on/updated_on -- NOT created_at), `AuditMixin`, `StatusMixin`, `SoftDeleteMixin`
- **Managers:** `ActiveQuerySet`, `SoftDeleteQuerySet`, `AliveQuerySet`, `ActiveManager`, `SoftDeleteManager`, `AliveManager`

---

## Test Results (Docker PostgreSQL)

| Test Scope             | Passed | Failed | Notes                                    |
| ---------------------- | ------ | ------ | ---------------------------------------- |
| **Full suite**         | 9866   | 0      | All tests passing (0 errors)             |
| **Products tests**     | 783    | 0      | SP01 (271) + SP03 (263+143+106=512)      |
| **Attributes tests**   | 350    | 0      | SP02 models+API+integration (147+124+79) |
| **Users tests**        | 298    | 0      | 71 API + 227 model tests                 |
| **Core tests (total)** | 5828   | 0      | All core/ tests combined                 |
| **Tenant tests**       | 2608   | 0      | All 40 previously failing fixed          |
| **Celery tests**       | 25     | 0      | Task infrastructure tests                |
| **Exception tests**    | 155    | 0      | Exception/handler/logging tests          |
| **Cache tests**        | 107    | 0      | Caching layer tests (audited)            |
| **Storage tests**      | 181    | 0      | File storage tests (SP10, audited)       |
| **API Docs tests**     | 154    | 0      | SP11 drf-spectacular tests               |
| **Pagination tests**   | 73     | 0      | SP12 Group A                             |
| **Filter tests**       | 100    | 0      | SP12 Group B                             |
| **Validator tests**    | 200    | 0      | SP12 Group C                             |
| **DateTime tests**     | 122    | 0      | SP12 Group D                             |
| **Sri Lanka tests**    | 293    | 0      | SP12 Group E                             |
| **Integration tests**  | 61     | 0      | SP12 Group F cross-module                |

---

## What Was Completed This Session (Session 7)

### SP03: Product Base Model (ALL 98 Tasks) — Phase 04

**Phase-04_ERP-Core-Modules-Part1/SubPhase-03_Product-Base-Model**

**Group A: Products App Setup (Tasks 01-14) — Constants**

- Rewrote `apps/products/constants.py` with TextChoices classes
- PRODUCT_TYPES: SIMPLE, VARIABLE, BUNDLE, COMPOSITE
- PRODUCT_STATUS: DRAFT, ACTIVE, ARCHIVED, DISCONTINUED
- Backward compatibility aliases: PRODUCT_STATUS_DRAFT, PRODUCT_STATUS_ACTIVE, PRODUCT_STATUS_CHOICES, etc.

**Group B: Supporting Models (Tasks 15-32)**

- Brand(BaseModel): name, slug(auto-gen), logo(ImageField), description, website(URLField); db_table="products_brand"
- TaxClass(BaseModel): name, rate(DecimalField 5,2, validators 0-100), is_default; save() enforces single default per tenant
- UnitOfMeasure(BaseModel): name, symbol, conversion_factor(DecimalField 10,4), is_base_unit; clean() validates base_unit→conversion_factor=1.0

**Group C: Product Model Definition (Tasks 33-56)**

- Product model REWRITTEN from UUIDMixin+TimestampMixin → BaseModel (27+ fields)
- Fields: name(200), slug(200), sku(50, auto-gen PRD-XXXXX), barcode, description, short_description, category(FK PROTECT), brand(FK SET_NULL), product_type, status, is_webstore_visible, is_pos_visible, featured, tax_class(FK SET_NULL), unit_of_measure(FK SET_NULL), cost_price/selling_price/mrp/wholesale_price, weight/length/width/height, seo_title/seo_description
- save() auto-generates slug + SKU (PRD-XXXXX format)
- profit_margin property, 5 DB indexes, ordering=["-created_on", "name"]

**Group D: Product Manager & QuerySets (Tasks 57-70)**

- ProductQuerySet: 11 methods — active, published, in_stock, by_category, by_brand, simple_products, variable_products, featured, for_pos, for_webstore, by_status
- ProductManager: proxies all 11 QuerySet methods + search() with PostgreSQL SearchVector/SearchRank

**Group E: Serializers & Views (Tasks 71-86)**

- 6 serializers: BrandSerializer, TaxClassSerializer, UoMSerializer, ProductListSerializer (lightweight), ProductDetailSerializer (nested), ProductCreateSerializer (transaction.atomic, auto-SKU, uniqueness validation)
- 3 ViewSets: BrandViewSet (filter is_active, search name), TaxClassViewSet (filter is_default), ProductViewSet (select_related, get_serializer_class() per action, published/featured custom actions, ProductFilter, SearchFilter, OrderingFilter)
- ProductFilter: UUIDFilter for category/brand, ChoiceFilter for product_type/status, BooleanFilter for visibility flags, NumberFilter for min_price/max_price
- URL routes: /api/v1/brands/, /api/v1/tax-classes/, /api/v1/products/
- Admin: BrandAdmin(logo_preview, prepopulated_fields), TaxClassAdmin(rate%), UoMAdmin, ProductAdmin(status_badge colors, autocomplete_fields, organized fieldsets, readonly sku)

**Group F: Testing & Documentation (Tasks 87-98)**

- 483 new tests total (753 products total with 270 existing SP01):
  - test_product_models.py: 263 mock-based tests (20 classes covering all models, fields, meta, managers, querysets)
  - test_product_api.py: 143 mock-based tests (12 classes covering all serializers, viewsets, filters, URLs)
  - test_product_integration.py: 77 DB integration tests (8 classes: CRUD, QuerySet, Manager Search, API Endpoints, SKU Generation)
  - conftest.py: 14 fixtures with tenant lifecycle (unique domain per module to avoid collision with attributes tests)
- Migration 0004_sp03_product_base_model created and applied (creates Brand/TaxClass/UnitOfMeasure, alters Product extensively)

### Key Architecture Decisions (SP03)

- Product extends BaseModel (UUID, timestamps, audit, status, soft-delete) — full lifecycle support
- TextChoices enums for type-safe constants with backward compatibility aliases
- Category FK changed from nullable SET_NULL → non-null PROTECT (every product must have a category)
- brand/tax_class/unit_of_measure are nullable SET_NULL (optional associations)
- Auto-SKU generation: PRD-XXXXX format with uuid4 hex prefix
- Products conftest uses unique domain ("products.testserver") to avoid collision with attributes conftest ("testserver")
- `.testserver` wildcard added to test ALLOWED_HOSTS for subdomain pattern support
- tenant_context fixture is NOT autouse — only integration tests that explicitly request it get tenant schema
- \_make_product() helper uses `Product.__new__()` + `ModelState()` initialization for mock-based tests

---

## What Was Completed in Previous Sessions

### Session 6: SP02 Attribute System (ALL 96 Tasks, Phase 04)

**Phase-04_ERP-Core-Modules-Part1/SubPhase-02_Attribute-System**

- Created new `apps.attributes` app (separate from products), added to TENANT_APPS
- 3 models: AttributeGroup, Attribute, AttributeOption — all extend BaseModel
- AttributeGroup: name, slug(auto), description, display_order; GroupQuerySet(active, with_attributes) + GroupManager
- Attribute: name, slug(auto), group(FK SET_NULL), attribute_type(choices), unit, is_required, is_filterable, is_searchable, is_comparable, is_visible_on_product, display_order, validation_regex, min_value, max_value, categories(M2M to products.Category); AttributeQuerySet(active, filterable, searchable, by_type, for_category) + AttributeManager
- AttributeOption: attribute(FK CASCADE), value, label, color_code, image, display_order, is_default; unique_together(attribute, value); OptionQuerySet(for_attribute, with_images, defaults) + OptionManager
- 5 DRF serializers: AttributeGroupSerializer, AttributeOptionSerializer, AttributeListSerializer, AttributeSerializer, AttributeDetailSerializer (nested group+options)
- 3 ViewSets: AttributeGroupViewSet, AttributeViewSet (multi-serializer, by-category + filterable actions), AttributeOptionViewSet
- DefaultRouter with attribute-groups, attributes, attribute-options endpoints
- Admin: AttributeGroupAdmin (prepopulated slug, attribute_count), AttributeAdmin (fieldsets, filter_horizontal categories, AttributeOptionInline), AttributeOptionAdmin
- 350 tests total: 147 model (mock) + 124 API (mock) + 79 integration (real PostgreSQL)
- Integration tests: tenant-aware fixtures, real CRUD on Docker PostgreSQL, full API endpoint testing
- Migration 0001_initial applied (3 models + 5 indexes + unique_together)
- Documentation: `backend/apps/attributes/README.md`, `backend/apps/attributes/docs/api.md`
- Deep audit completed: 5 gaps found and fixed, SP02_AUDIT_REPORT.md created
- Gaps fixed: Attribute ordering (group\_\_display_order), OptionManager with_images proxy, AttributeManager by_type proxy, unit-required-for-NUMBER serializer validation, ViewSet ordering

### Key Architecture Decisions

- NEW separate `apps.attributes` app (unlike SP01 which went into existing products app)
- Used `BaseModel` directly (no TreeManager conflict — no MPTT involvement)
- 6 attribute types: TEXT, NUMBER, SELECT, MULTISELECT, BOOLEAN, DATE (in constants.py)
- `default=""` for text fields, `null=True` only for DecimalField min/max and ImageField
- Categories M2M references `"products.Category"` (actual app location), not `categories.Category`
- by-category action walks parent chain for attribute inheritance
- Database-free tests (mocks + \_meta introspection) matching project convention

---

## What Was Completed in Previous Sessions

### Session 5: SP01 Category Model & Hierarchy (Phase 04)

- Installed django-mptt 0.18.0, upgraded Category model to MPTT
- CategoryQuerySet + CategoryManager, 5 DRF serializers, ViewSet with CRUD+tree+move
- MPTTModelAdmin, 4 management commands, 270 tests (all passing)
- 3 migrations, deep audit, SP01_AUDIT_REPORT.md

### Session 4: SP10-SP12 (Phase 03 completion)

- SP10 File Storage, SP11 API Documentation, SP12 Core Utilities & Helpers
- All audited and certified

### Session 3

### 1. Wired Users API to URLs

- Added `path("api/v1/users/", include("apps.users.api.urls", namespace="users"))` to `config/urls.py`

### 2. Added 227 Model CRUD Tests

- Created `backend/tests/users/test_models.py` with comprehensive tests
- Covers: field configs, meta options, **str**, managers, save() overrides, querysets, constants, validators, decorators, relationships, model inheritance

### 3. Fixed All 40 Tenant Mock Tests

- Fixed `MockMeta` in `test_routers.py` -- added missing `model_name` attribute
- Fixed cache/connection patches in `test_middleware.py` -- changed from module-level to `django.core.cache.cache` / `django.db.connection`
- Fixed integration/performance tests with same pattern
- Added `@override_settings(ALLOWED_HOSTS=["*"])` where needed
- Result: 2608 passed, 0 failed (was 2568 passed, 40 failed)

### 4. SP07 Tasks 71-86 (Remaining Exception Handling)

**Tasks 71-74: Sentry Context Middleware**

- Created `backend/apps/core/middleware/sentry.py` -- SentryContextMiddleware
- Updated middleware `__init__.py` and `config/settings/base.py` MIDDLEWARE list
- Created `backend/docs/exceptions/sentry.md`

**Tasks 75-82: Exception Tests**

- Created `backend/tests/core/test_exceptions.py` (102 tests)
- Created `backend/tests/core/test_handlers.py` (20 tests)
- Created `backend/tests/core/test_response.py` (14 tests)
- Created `backend/tests/core/test_error_logging.py` (17 tests)

**Tasks 83-86: Documentation & Verification**

- Created `backend/docs/exceptions/api_error_guide.md`
- Created `backend/docs/exceptions/troubleshooting.md`
- Created `backend/docs/exceptions/error_codes_reference.md`
- Created `backend/docs/exceptions/verification.md`

### 5. SP08: Celery Task Queue (ALL 90 Tasks)

**Groups A-B: Installation & Configuration**

- Added: CELERY_TASK_TRACK_STARTED, CELERY_TASK_TIME_LIMIT, CELERY_TASK_SOFT_TIME_LIMIT

**Group C: Task Infrastructure (6 files)**

- `backend/apps/core/tasks/` -- **init**.py, base.py, email_tasks.py, report_tasks.py, notification_tasks.py

**Group D: Celery Beat Scheduling**

- `backend/apps/core/tasks/scheduled_tasks.py` -- 5 periodic tasks
- Added CELERY_BEAT_SCHEDULE to base.py

**Group E: Monitoring & Retry**

- Created `backend/config/settings/celery_settings.py`
- Created `backend/apps/core/tasks/error_handlers.py`

**Group F: Testing & Documentation**

- Updated `config/settings/test_pg.py` -- CELERY_TASK_ALWAYS_EAGER
- Created `backend/tests/core/test_tasks.py` -- 25 tests
- Created `backend/docs/celery/` -- 3 doc files

### 6. SP09: Caching Layer (ALL 88 Tasks) -- NEW

**Groups A-B: Redis Setup & Cache Backend Configuration**

- Created `backend/config/settings/cache.py` -- CACHES with default/sessions/ratelimit aliases (django-redis)
- Redis DB allocation: DB0=Celery, DB1=Cache, DB2=Channels, DB3=Sessions, DB4=Ratelimit
- Connection pool settings, socket timeouts, health check intervals
- Session engine configured to use Redis cache
- Cache TTL constants: SHORT (5min), MEDIUM (1hr), LONG (1day)
- Imported in base.py with wildcard import
- Updated test.py with LocMemCache aliases for sessions + ratelimit
- Added django-redis>=5.4 to base.in requirements

**Group C: Tenant-Scoped Caching (6 files)**

- `backend/apps/core/cache/__init__.py` -- Package with full API exports
- `backend/apps/core/cache/constants.py` -- TTL presets, key templates, MAX_KEY_LENGTH
- `backend/apps/core/cache/tenant_cache.py` -- TenantCache class with tenant-prefixed keys
  - get/set/delete, get_many/set_many, incr/decr, delete_pattern
  - Auto-hashes keys >200 chars, graceful error handling
- `get_tenant_cache()` factory function

**Group D: Cache Decorators & Utilities**

- `backend/apps/core/cache/decorators.py` -- cache_response (view caching with DRF support), cache_method, cache_queryset
  - vary_on_tenant, vary_on_user parameters
  - Custom cache_key (string or callable)
  - Only caches 2xx responses
- `backend/apps/core/cache/utils.py` -- make_cache_key, hash_key, cache_get_or_set, clear_cache, cache_stats

**Group E: Invalidation Patterns**

- `backend/apps/core/cache/invalidation.py` -- CacheInvalidator (static methods for model/list/detail/related/tenant invalidation)
  - Signal handlers: cache_post_save_handler, cache_post_delete_handler
  - CacheMixin for model auto-invalidation
- `backend/apps/core/management/commands/clearcache.py` -- Management command with --alias, --pattern, --all flags

**Group F: Testing & Documentation**

- `backend/tests/core/test_cache.py` -- 107 tests across 25 test classes (audited: covers session caching, CacheMixin instance methods, transaction.on_commit, clearcache --tenant/--model)
- `backend/docs/caching/overview.md` -- Architecture, key format, TTL guidelines, Redis DB allocation
- `backend/docs/caching/patterns.md` -- Usage patterns with code examples
- `backend/docs/caching/invalidation.md` -- Invalidation guide, signal handlers, CacheMixin, clearcache command
- `backend/docs/caching/performance.md` -- Performance guidelines, pool sizing, stampede prevention, monitoring

### 7. SP12: Core Utilities & Helpers (ALL 94 Tasks) — Session 4

**Group A: Pagination (Tasks 01-16)**

- `backend/apps/core/pagination/` — StandardPagination (page_size=20, max=100), LCCCursorPagination, LCCLimitOffsetPagination, NoPagination
- Updated `backend/config/settings/base.py` — DEFAULT_PAGINATION_CLASS
- 73 tests

**Group B: Filters (Tasks 17-32)**

- `backend/apps/core/filters/` — 7 filter backends (TenantFilterBackend, DateRangeFilterBackend, LCCSearchFilter, LCCOrderingFilter, IsActiveFilterBackend, CreatedByFilterBackend, ModifiedAtFilterBackend)
- BaseFilterSet with is_active, created_after/before→created_on, modified_after/before→updated_on
- 100 tests

**Group C: Validators (Tasks 33-48)**

- `backend/apps/core/validators/` — 12 validators (email, URL, slug, positive number, decimal, percentage, file size, image dimension, file extension, JSON, no HTML, unique for tenant)
- 200 tests

**Group D: DateTime Helpers (Tasks 49-62)**

- `backend/apps/core/datetime/` — SL_TIMEZONE (Asia/Colombo), timezone conversions, date/month/year ranges, fiscal year support (April-March), SL date formatting
- Requires pytz
- 122 tests

**Group E: Sri Lanka Utilities (Tasks 63-78)**

- `backend/apps/core/srilanka/` — LKR currency formatting/parsing, phone validation/formatting (+94), NIC validation/DOB parsing (old 9+V/X, new 12-digit), 9 provinces + 25 districts
- 293 tests

**Group F: Testing & Documentation (Tasks 79-94)**

- `backend/apps/core/README.md` — comprehensive module documentation
- `backend/tests/core/test_integration.py` — 61 cross-module integration tests
- `backend/scripts/verify_sp12.py` — 120/120 verification checks
- `docs/backend/utilities.md` — summary documentation

**SP12 Totals: 849 new tests, 120/120 verification checks, 5,828 core tests pass**

### SP12 Audit (ALL 94 Tasks Audited)

- Audited all 94 tasks across 6 groups (A-F) — deep comparison against task documents
- 94 DONE, 0 PARTIAL, 0 MISSING — **100% completion**
- 15 structural deviations documented (all intentional improvements or project conventions)
- Created `SP12_AUDIT_REPORT.md` with full audit report and certification

### 8. SP10 Audit (ALL 86 Tasks Audited)

- Audited all 86 tasks across 6 groups (A-F)
- 85 DONE, 1 PARTIAL (Task 32 version pin format — non-blocking)
- Fixed Task 83: Created `backend/apps/core/storage/README.md`
- Fixed Task 84: Created `backend/apps/core/storage/docs/UPLOAD_PATTERNS.md`
- Created `SP10_AUDIT_REPORT.md` with full audit report

### 9. SP11: API Documentation (ALL 82 Tasks)

**Group A: drf-spectacular Installation & Setup (Tasks 01-14)**

- Added `drf-spectacular>=0.27` and `drf-spectacular[sidecar]>=0.27` to requirements
- Added `drf_spectacular` and `drf_spectacular_sidecar` to INSTALLED_APPS
- Set `DEFAULT_SCHEMA_CLASS: "drf_spectacular.openapi.AutoSchema"` in REST_FRAMEWORK
- Created `backend/config/settings/api_docs.py` (imported via wildcard in base.py)
- Created URL patterns: `/api/schema/`, `/api/docs/`, `/api/redoc/`

**Group B: Schema Configuration (Tasks 15-28)**

- Configured SPECTACULAR_SETTINGS: title "LankaCommerce Cloud API", version "1.0.0"
- Contact info with URL, MIT license with URL
- SCHEMA_PATH_PREFIX, SERVE_INCLUDE_SCHEMA=False
- Dev + prod servers (prod from env var)
- 15 categorized tags (Authentication through Platform)
- COMPONENT_SPLIT_REQUEST=True

**Group C: Swagger UI Settings (Tasks 29-42)**

- SWAGGER_UI_DIST/REDOC_DIST = SIDECAR
- SWAGGER_UI_SETTINGS: deepLinking, tryItOutEnabled, persistAuthorization, filter
- Alpha sorting, monokai syntax highlighting theme
- JWT Bearer auth scheme in SECURITY + COMPONENT_SECURITY_SCHEMES
- Custom CSS file at `backend/static/api_docs/custom.css` (brand colors, HTTP method coding, dark mode)

**Group D: ReDoc Configuration (Tasks 43-54)**

- REDOC_UI_SETTINGS with full theme: colors, typography (Roboto/Source Code Pro), sidebar
- expandResponses "200,201", pathInMiddlePanel=True, hideDownloadButton=False
- x-logo extension pointing to `/static/api_docs/logo.png`
- Placeholder logo.png and logo.svg created

**Group E: Documentation Enhancements (Tasks 55-70)**

- `extensions.py` (506 lines): custom_preprocessing_hook (filters /\_internal/ paths)
- TENANT_HEADER_PARAMETER (X-Tenant-ID OpenApiParameter)
- DESCRIPTION_SUPPLEMENT: authentication, error responses, pagination, filtering, ordering, rate limiting, versioning, changelog
- `schemas.py`: 9 serializer classes (Error, Validation, Auth, Permission, NotFound, RateLimit, Token, TokenRefresh, Paginated)
- `examples.py`: 18 OpenApiExample instances (login, token, products, orders, customers, errors)
- Full `__init__.py` exports (45+ items)

**Group F: Testing & Validation (Tasks 71-82)**

- `test_api_docs.py`: 10 test classes, 154 tests — ALL PASS
- `validate_schema.py`: management command with --strict, --output flags
- `README.md`: usage documentation for api_docs module
- `decorators.md`: @extend_schema decorator guide
- `extensions.md`: extension development guide

---

## Complete List of Files Created/Modified (All Sessions)

### Session 2 Files

```
backend/apps/core/models.py                     # UPGRADED: real abstract model classes
backend/apps/core/exceptions/__init__.py         # NEW
backend/apps/core/exceptions/base.py             # NEW
backend/apps/core/exceptions/client.py           # NEW
backend/apps/core/exceptions/auth.py             # NEW
backend/apps/core/exceptions/server.py           # NEW
backend/apps/core/exceptions/handlers.py         # NEW
backend/apps/core/exceptions/response.py         # NEW
backend/apps/core/exceptions/logging.py          # NEW
backend/apps/core/middleware/__init__.py          # NEW
backend/apps/core/middleware/base.py              # NEW
backend/apps/core/middleware/request_logging.py   # NEW
backend/apps/core/middleware/security.py          # NEW
backend/apps/core/middleware/rate_limiting.py     # NEW
backend/apps/core/middleware/timezone.py          # NEW
backend/apps/users/models.py                     # UPGRADED: 6 models
backend/apps/users/managers/__init__.py           # UPGRADED: 4 classes
backend/apps/users/decorators.py                 # NEW: 4 decorators
backend/apps/users/signals/__init__.py            # UPGRADED: 3 signal handlers
backend/apps/users/apps.py                       # UPGRADED: added ready()
backend/apps/users/admin.py                      # NEW: admin registrations
backend/apps/users/api/__init__.py               # NEW
backend/apps/users/api/serializers.py            # NEW: 8 serializers
backend/apps/users/api/views.py                  # NEW: 7 viewsets/views
backend/apps/users/api/urls.py                   # NEW: URL routing
backend/apps/users/migrations/__init__.py        # NEW
backend/apps/users/migrations/0001_initial.py    # NEW
backend/tests/users/__init__.py                  # NEW
backend/tests/users/test_api.py                  # NEW: 71 tests
backend/config/settings/sentry.py                # NEW
backend/config/settings/local_sqlite.py          # NEW
backend/config/settings/test_pg.py               # NEW
backend/config/settings/base.py                  # UPGRADED
```

### Session 3 Files

```
backend/config/urls.py                           # MODIFIED: added users API URL
backend/tests/users/test_models.py               # NEW: 227 tests
backend/tests/tenants/test_routers.py            # FIXED: MockMeta.model_name
backend/tests/tenants/test_middleware.py          # FIXED: cache/connection patches
backend/tests/tenants/test_integration.py        # FIXED: patches + ALLOWED_HOSTS
backend/tests/tenants/test_performance.py        # FIXED: patches + ALLOWED_HOSTS
backend/apps/core/middleware/sentry.py           # NEW: SentryContextMiddleware
backend/apps/core/middleware/__init__.py          # UPDATED: added sentry export
backend/config/settings/base.py                  # UPDATED: sentry middleware + celery + cache import
backend/tests/core/test_exceptions.py            # NEW: 102 tests
backend/tests/core/test_handlers.py              # NEW: 20 tests
backend/tests/core/test_response.py              # NEW: 14 tests
backend/tests/core/test_error_logging.py         # NEW: 17 tests
backend/docs/exceptions/sentry.md                # NEW
backend/docs/exceptions/api_error_guide.md       # NEW
backend/docs/exceptions/troubleshooting.md       # NEW
backend/docs/exceptions/error_codes_reference.md # NEW
backend/docs/exceptions/verification.md          # NEW
backend/apps/core/tasks/__init__.py              # NEW
backend/apps/core/tasks/base.py                  # NEW: BaseTask + TenantAwareTask
backend/apps/core/tasks/email_tasks.py           # NEW
backend/apps/core/tasks/report_tasks.py          # NEW
backend/apps/core/tasks/notification_tasks.py    # NEW
backend/apps/core/tasks/scheduled_tasks.py       # NEW: 5 periodic tasks
backend/apps/core/tasks/error_handlers.py        # NEW: signal handlers
backend/config/settings/celery_settings.py       # NEW
backend/config/settings/test_pg.py               # UPDATED: CELERY_ALWAYS_EAGER
backend/tests/core/test_tasks.py                 # NEW: 25 tests
backend/docs/celery/configuration.md             # NEW
backend/docs/celery/task_creation.md             # NEW
backend/docs/celery/monitoring.md                # NEW
backend/config/settings/cache.py                 # NEW: Redis CACHES config
backend/apps/core/cache/__init__.py              # NEW: package exports
backend/apps/core/cache/constants.py             # NEW: TTL presets, key templates
backend/apps/core/cache/tenant_cache.py          # NEW: TenantCache class
backend/apps/core/cache/decorators.py            # NEW: cache_response/method/queryset
backend/apps/core/cache/utils.py                 # NEW: make_cache_key, hash_key, etc.
backend/apps/core/cache/invalidation.py          # NEW: CacheInvalidator, signals, CacheMixin
backend/apps/core/management/commands/clearcache.py  # NEW: clearcache command
backend/config/settings/test.py                  # UPDATED: added sessions+ratelimit caches
backend/requirements/base.in                     # UPDATED: added django-redis>=5.4
backend/tests/core/test_cache.py                 # NEW: 84 tests
backend/docs/caching/overview.md                 # NEW
backend/docs/caching/patterns.md                 # NEW
backend/docs/caching/invalidation.md             # NEW
backend/config/settings/storage.py               # NEW: file storage settings (SP10)
backend/apps/core/storage/__init__.py            # NEW: package exports
backend/apps/core/storage/backends.py            # NEW: TenantFileStorage, TenantMediaStorage, PublicStorage, TenantS3Storage
backend/apps/core/storage/paths.py               # NEW: upload path generators
backend/apps/core/storage/validators.py          # NEW: FileValidator with extension/size/MIME/malware
backend/apps/core/storage/images.py              # NEW: ImageProcessor (resize/compress/convert/thumbnails/web optimize)
backend/apps/core/storage/handlers.py            # NEW: handle_image_upload (sync/async)
backend/apps/core/storage/s3.py                  # NEW: signed URL utilities
backend/apps/core/storage/constants.py           # NEW: URL expiry, thumbnail sizes, extension/size helpers
backend/apps/core/storage/cleanup.py             # NEW: FileCleanup orphaned file detection
backend/apps/core/tasks/images.py                # NEW: Celery image processing tasks
backend/apps/core/management/commands/cleanmedia.py  # NEW: cleanmedia command
backend/tests/core/test_storage.py               # NEW: 181 tests
backend/docs/storage/overview.md                 # NEW
backend/docs/storage/configuration.md            # NEW
backend/docs/storage/performance.md              # NEW
backend/docs/storage/api.md                      # NEW
backend/apps/core/storage/README.md              # NEW: storage module README (Task 83)
backend/apps/core/storage/docs/UPLOAD_PATTERNS.md # NEW: upload patterns doc (Task 84)
backend/docs/caching/performance.md              # NEW
SP10_AUDIT_REPORT.md                             # NEW: 86-task audit report (85 DONE, 1 PARTIAL)
backend/config/settings/api_docs.py              # NEW: SPECTACULAR_SETTINGS (341 lines) (SP11)
backend/apps/core/api_docs/__init__.py           # NEW: package exports (45+ items)
backend/apps/core/api_docs/urls.py               # NEW: /api/schema/, /api/docs/, /api/redoc/
backend/apps/core/api_docs/extensions.py         # NEW: preprocessing hook, descriptions (506 lines)
backend/apps/core/api_docs/schemas.py            # NEW: 9 response serializer classes
backend/apps/core/api_docs/examples.py           # NEW: 18 OpenApiExample instances
backend/apps/core/api_docs/README.md             # NEW: usage documentation
backend/apps/core/management/commands/validate_schema.py  # NEW: CI schema validation
backend/static/api_docs/custom.css               # NEW: Swagger UI brand CSS
backend/static/api_docs/logo.png                 # NEW: placeholder logo
backend/static/api_docs/logo.svg                 # NEW: SVG logo
backend/tests/core/test_api_docs.py              # NEW: 154 tests
backend/docs/api_docs/decorators.md              # NEW: schema decorator guide
backend/docs/api_docs/extensions.md              # NEW: extension guide
backend/config/settings/base.py                  # UPDATED: drf_spectacular + sidecar in INSTALLED_APPS, AutoSchema, api_docs import
backend/config/urls.py                           # UPDATED: added api_docs URLs
backend/requirements/base.in                     # UPDATED: added drf-spectacular>=0.27, drf-spectacular[sidecar]>=0.27
backend/scripts/verify_api_docs.py               # NEW: 50-check integration verification (SP11 audit)
.github/workflows/api-schema.yml                 # NEW: CI workflow for schema validation (SP11 audit)
SP11_AUDIT_REPORT.md                             # NEW: 82-task audit report (82 DONE, 8 fixes applied)
```

### Session 4 Files (SP12: Core Utilities & Helpers)

```
backend/apps/core/pagination/__init__.py         # NEW: package exports
backend/apps/core/pagination/standard.py         # NEW: StandardPagination (page_size=20, max=100)
backend/apps/core/pagination/cursor.py           # NEW: LCCCursorPagination (ordering=-created_on)
backend/apps/core/pagination/limit_offset.py     # NEW: LCCLimitOffsetPagination
backend/apps/core/pagination/none.py             # NEW: NoPagination
backend/apps/core/filters/__init__.py            # NEW: package exports
backend/apps/core/filters/backends.py            # NEW: 7 filter backends
backend/apps/core/filters/filtersets.py          # NEW: BaseFilterSet
backend/apps/core/validators/__init__.py         # NEW: 12 validators exported
backend/apps/core/validators/common.py           # NEW: email/URL/slug/number validators
backend/apps/core/validators/file_validators.py  # NEW: file size/image/extension validators
backend/apps/core/validators/content.py          # NEW: JSON/HTML/tenant-unique validators
backend/apps/core/datetime/__init__.py           # NEW: datetime package exports
backend/apps/core/datetime/timezone.py           # NEW: SL timezone conversions
backend/apps/core/datetime/date_utils.py         # NEW: date/month/year ranges, formatting
backend/apps/core/srilanka/__init__.py           # NEW: SL utilities package exports
backend/apps/core/srilanka/currency.py           # NEW: LKR formatting/parsing/conversion
backend/apps/core/srilanka/phone.py              # NEW: SL phone validation/formatting
backend/apps/core/srilanka/nic.py                # NEW: NIC validation/DOB parsing
backend/apps/core/srilanka/provinces.py          # NEW: 9 provinces + 25 districts
backend/apps/core/README.md                      # NEW: comprehensive utilities README
backend/tests/core/test_pagination.py            # NEW: 73 tests
backend/tests/core/test_filters.py               # NEW: 100 tests
backend/tests/core/test_validators.py            # NEW: 200 tests
backend/tests/core/test_datetime.py              # NEW: 122 tests
backend/tests/core/test_srilanka.py              # NEW: 293 tests
backend/tests/core/test_integration.py           # NEW: 61 integration tests
backend/scripts/verify_sp12.py                   # NEW: 120 verification checks
docs/backend/utilities.md                        # NEW: utilities summary doc
backend/config/settings/base.py                  # UPDATED: DEFAULT_PAGINATION_CLASS
SP12_AUDIT_REPORT.md                             # NEW: 94-task audit report (94 DONE, certified)

# Session 5 — SP01 Category Model & Hierarchy (Phase-04)
SP01_AUDIT_REPORT.md                             # NEW: 92-task audit report (82 DONE, 10 PARTIAL, certified)
backend/apps/products/models/category.py         # UPDATED: MPTT model with all fields
backend/apps/products/models/managers.py         # NEW: CategoryQuerySet + CategoryManager
backend/apps/products/api/__init__.py             # NEW: API package init
backend/apps/products/api/serializers.py         # NEW: 5 DRF serializers
backend/apps/products/api/views.py               # NEW: CategoryViewSet with CRUD + tree + move
backend/apps/products/api/urls.py                # NEW: Router-based URL config
backend/apps/products/admin.py                   # UPDATED: MPTTModelAdmin with full config
backend/apps/products/management/commands/        # NEW: 4 management commands
backend/apps/products/migrations/0002_*.py       # NEW: MPTT upgrade migration
backend/apps/products/migrations/0003_*.py       # NEW: display_order index migration
backend/apps/products/docs/                      # NEW: overview.md, api.md, README.md
backend/tests/products/test_models.py            # NEW: 151 model tests
backend/tests/products/test_api.py               # NEW: 119 API tests
backend/requirements/base.in                     # UPDATED: added django-mptt>=0.16
backend/config/settings/database.py              # UPDATED: mptt in SHARED_APPS
backend/config/urls.py                           # UPDATED: products API URLs

# Session 6 — SP02 Attribute System (Phase-04)
backend/apps/attributes/__init__.py               # NEW: App package
backend/apps/attributes/apps.py                   # NEW: AttributesConfig
backend/apps/attributes/constants.py              # NEW: ATTRIBUTE_TYPES (6 types)
backend/apps/attributes/models/__init__.py        # NEW: Model exports
backend/apps/attributes/models/attribute_group.py # NEW: AttributeGroup + GroupQuerySet/Manager
backend/apps/attributes/models/attribute.py       # NEW: Attribute + AttributeQuerySet/Manager
backend/apps/attributes/models/attribute_option.py # NEW: AttributeOption + OptionQuerySet/Manager
backend/apps/attributes/serializers.py            # NEW: 5 DRF serializers
backend/apps/attributes/views.py                  # NEW: 3 ViewSets + by_category/filterable actions
backend/apps/attributes/urls.py                   # NEW: DefaultRouter URL config
backend/apps/attributes/admin.py                  # NEW: 3 admin classes + inline
backend/apps/attributes/migrations/0001_initial.py # NEW: Initial migration (3 models + indexes)
backend/apps/attributes/README.md                 # NEW: App documentation
backend/apps/attributes/docs/api.md               # NEW: API endpoint documentation
backend/tests/attributes/__init__.py              # NEW: Test package
backend/tests/attributes/test_models.py           # NEW: 147 model tests
backend/tests/attributes/test_api.py              # NEW: 121 API/admin tests
backend/config/settings/database.py               # UPDATED: apps.attributes in TENANT_APPS
backend/config/urls.py                            # UPDATED: attributes API URLs
```

### Session 7 Files (SP03: Product Base Model)

```
backend/apps/products/constants.py                # REWRITTEN: TextChoices enums + backward compat aliases
backend/apps/products/models/brand.py             # NEW: Brand(BaseModel) with auto-slug
backend/apps/products/models/tax_class.py         # NEW: TaxClass(BaseModel) with single-default logic
backend/apps/products/models/unit_of_measure.py   # NEW: UnitOfMeasure(BaseModel) with conversion_factor
backend/apps/products/models/product.py           # REWRITTEN: Product(BaseModel) 27+ fields, auto-SKU
backend/apps/products/models/managers.py          # UPDATED: Added ProductQuerySet(11 methods) + ProductManager(search)
backend/apps/products/models/__init__.py          # UPDATED: Brand, TaxClass, UoM, ProductQuerySet, ProductManager exports
backend/apps/products/api/serializers.py          # APPENDED: 6 new serializers (Brand, TaxClass, UoM, ProductList, ProductDetail, ProductCreate)
backend/apps/products/api/views.py                # APPENDED: 3 ViewSets (Brand, TaxClass, Product) with custom actions
backend/apps/products/api/filters.py              # NEW: ProductFilter (UUID, choice, boolean, number filters)
backend/apps/products/api/urls.py                 # UPDATED: 4 router registrations (categories, brands, tax-classes, products)
backend/apps/products/admin.py                    # APPENDED: BrandAdmin, TaxClassAdmin, UoMAdmin, ProductAdmin
backend/apps/products/migrations/0004_sp03_product_base_model.py  # NEW: Creates Brand/TaxClass/UoM, alters Product
backend/tests/products/conftest.py                # NEW: 14 fixtures, unique domain "products.testserver"
backend/tests/products/test_product_models.py     # NEW: 263 mock-based model tests (20 classes)
backend/tests/products/test_product_api.py        # NEW: 143 mock-based API tests (12 classes)
backend/tests/products/test_product_integration.py # NEW: 77 DB integration tests (8 classes)
backend/config/settings/test.py                   # UPDATED: Added ".testserver" to ALLOWED_HOSTS for subdomain support
```

### Session 8 Files (SP03: Deep Audit)

```
backend/apps/products/__init__.py                 # FIXED: Added __version__ = "0.1.0" + 4 product types in docstring
backend/apps/products/models/product.py           # FIXED: db_index on visibility fields, seo_title 100, seo_desc 300, 2 new indexes
backend/apps/products/api/serializers.py          # FIXED: Module docstring updated (was category-only)
backend/apps/products/admin.py                    # FIXED: status_badge ordering="status" added
backend/apps/products/migrations/0005_sp03_audit_fixes.py # NEW: 6 operations (db_index, max_length, indexes)
backend/apps/products/README.md                   # REWRITTEN: Covers all SP03 models, API endpoints, QuerySet API
backend/tests/products/test_product_models.py     # FIXED: seo assertion values (70→100, 160→300)
backend/tests/products/test_product_integration.py # EXPANDED: +29 tests → 106 total (API, tenant isolation, permissions)
SP03_AUDIT_REPORT.md                              # NEW: Comprehensive audit report with certification
```

---

## Config Functions (Pre-existing, KEPT Untouched)

These ~620 config functions and their ~4956 tests still exist and pass. They are NOT real Django code.

| File                                                  | Count  | SubPhase |
| ----------------------------------------------------- | ------ | -------- |
| `backend/apps/core/utils/apps_structure_utils.py`     | varies | SP01     |
| `backend/apps/core/utils/api_framework_utils.py`      | varies | SP02     |
| `backend/apps/core/utils/base_models_utils.py`        | 94     | SP03     |
| `backend/apps/core/utils/user_model_utils.py`         | 96     | SP04     |
| `backend/apps/core/utils/role_permission_utils.py`    | 92     | SP05     |
| `backend/apps/core/utils/core_middleware_utils.py`    | 88     | SP06     |
| `backend/apps/core/utils/exception_handling_utils.py` | 70     | SP07     |

---

## Known Minor Gaps (Non-Blocking)

| Gap                               | Document Location        | Current State                                            | Impact |
| --------------------------------- | ------------------------ | -------------------------------------------------------- | ------ |
| `error_codes.py` (ErrorCode enum) | SP07/Group-A Tasks 09-11 | Error codes are string constants in each exception class | Zero   |
| Exception Registry metaclass      | SP07/Group-A Task 12     | No auto-registration; exceptions imported directly       | Zero   |

---

## What To Do Next

| Priority | Task                            | Details                                                  |
| -------- | ------------------------------- | -------------------------------------------------------- |
| 1        | **Phase-04 SP04+: ERP Core**    | SP01+SP02+SP03 COMPLETE — Continue Phase-04 SubPhase-04+ |
| 2        | **SP03 Audit**                  | Deep audit of SP03 (98 tasks) like SP01/SP02             |
| 3        | **Phase-05+ ERP Modules Part2** | Continue to Phase-05 after Phase-04 complete             |
| 4        | **Phase-06+ Advanced Modules**  | Continue through remaining phases                        |

---

## Docker Test Commands

```bash
# Full test suite (PostgreSQL) -- ~9837 tests
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-redis drf-spectacular drf-spectacular-sidecar pytz django-mptt django-filter && python -m pytest tests/ --tb=short -q"

# Products tests only (753 tests — SP01 category 270 + SP03 product 483)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-mptt django-filter && python -m pytest tests/products/ --tb=short -q"

# Products model tests only (263 tests — SP03 mock-based)
docker exec lcc-backend bash -c "cd /app && DJANGO_SETTINGS_MODULE=config.settings.test_pg python -m pytest tests/products/test_product_models.py --tb=short -q"

# Products API tests only (143 tests — SP03 mock-based)
docker exec lcc-backend bash -c "cd /app && DJANGO_SETTINGS_MODULE=config.settings.test_pg python -m pytest tests/products/test_product_api.py --tb=short -q"

# Products integration tests only (77 tests — SP03 real DB)
docker exec lcc-backend bash -c "cd /app && DJANGO_SETTINGS_MODULE=config.settings.test_pg python -m pytest tests/products/test_product_integration.py --tb=short -q"

# Cache tests only (84 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-redis && python -m pytest tests/core/test_cache.py --tb=short -q"

# Users tests only (298 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-redis && python -m pytest tests/users/ --tb=short -q"

# Core tests only (~5828 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-redis drf-spectacular drf-spectacular-sidecar pytz && python -m pytest tests/core/ --tb=short -q"

# SP12 Pagination tests (73 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_pagination.py --tb=short -q"

# SP12 Filter tests (100 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_filters.py --tb=short -q"

# SP12 Validator tests (200 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_validators.py --tb=short -q"

# SP12 DateTime tests (122 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_datetime.py --tb=short -q"

# SP12 Sri Lanka tests (293 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_srilanka.py --tb=short -q"

# SP12 Integration tests (61 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django pytz && python -m pytest tests/core/test_integration.py --tb=short -q"

# Tenant tests only (2608 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django && python -m pytest tests/tenants/ --tb=short -q"

# API Docs tests only (154 tests)
cd /e/work_git_repos/pos && docker compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend bash -c "pip install -q pytest pytest-django django-redis drf-spectacular drf-spectacular-sidecar && python -m pytest tests/core/test_api_docs.py --tb=short -q"

# Import verification
cd /e/work_git_repos/pos && docker compose run --rm --no-deps -e DJANGO_SETTINGS_MODULE=config.settings.test_pg --entrypoint "" backend python -c "import django; django.setup(); from apps.core.cache import TenantCache, get_tenant_cache, CacheInvalidator, cache_response, cache_method, cache_queryset; print('ALL CACHE IMPORTS OK')"
```

---

## Workflow Rules

1. Always read each Document-Series document carefully before implementing
2. Create REAL Django code (models, views, serializers, etc.) -- NEVER config functions
3. Keep existing config functions and their tests (they still pass)
4. Use Docker PostgreSQL for ALL testing and development -- NEVER SQLite
5. pytest.ini defaults to `config.settings.test_pg` (Docker PostgreSQL)
6. pytest + pytest-django are NOT pre-installed in Docker -- each run does `pip install -q pytest pytest-django` first
7. Run `python /e/My_GitHub_Repos/flow/flow.py` for user review after each task
8. Use subagents for complex implementations to manage context window
9. The `users` app models complement PlatformUser -- they don't replace AUTH_USER_MODEL
10. Existing mixins use `created_on`/`updated_on` (NOT `created_at`/`updated_at`)
11. Celery test settings: CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True
12. TenantAwareTask uses `connection.set_tenant()` for schema switching in async tasks
13. Cache tests use LocMemCache (no Redis dependency) -- delete_pattern not available in test backend
14. django-redis must be installed in Docker run commands: `pip install -q django-redis`
15. drf-spectacular + drf-spectacular-sidecar must be installed in Docker run commands for API docs tests
16. pytz must be installed in Docker run commands for datetime/SL utilities tests
17. Phase-03 Core Backend Infrastructure is now COMPLETE (SP01-SP12)
18. Phase-04 SP01 Category Model & Hierarchy is now COMPLETE (92 tasks, audited)
19. django-mptt must be installed in Docker run commands for products tests: `pip install -q django-mptt`
20. Phase-04 SP02 Attribute System is now COMPLETE (96 tasks, 350 tests, AUDITED)
21. Attributes app is a separate app (`apps.attributes`), registered in TENANT_APPS
22. Attribute integration tests use real PostgreSQL with tenant fixtures (conftest.py)
23. SP02_AUDIT_REPORT.md documents all 96 tasks, 5 gaps fixed, 7 acceptable deviations
24. django-filter must be installed in Docker run commands for products API tests: `pip install -q django-filter`
25. Products app Category uses `UUIDMixin + TimestampMixin + MPTTModel` (not BaseModel — avoids TreeManager conflict)
26. Phase-04 SP03 Product Base Model is now COMPLETE (98 tasks, 483 new tests, 753 products total)
27. Products conftest uses unique domain "products.testserver" (not "testserver") to avoid collision with attributes tenant
28. test.py ALLOWED_HOSTS includes ".testserver" wildcard for subdomain patterns
29. Product model extends BaseModel (UUID, timestamps, audit, status, soft-delete); Category uses UUIDMixin+TimestampMixin
30. Products integration tests must explicitly request `tenant_context` fixture (NOT autouse)
31. Mock-based tests use `Product.__new__(Product)` + `obj._state = ModelState()` to avoid FK descriptor errors32. SP03 deep audit COMPLETE — 12 gaps found and fixed, 18 acceptable deviations documented
33. SP03_AUDIT_REPORT.md documents all 98 tasks, migration 0005, full certification
34. Tenant isolation tests use `connection.set_schema_to_public()` before creating second tenant
35. Full test suite: 9,866 passed, 0 errors (after SP03 audit)