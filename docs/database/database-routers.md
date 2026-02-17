# Database Router Configuration

> LankaCommerce Cloud — Schema-Aware Query and Migration Routing

---

## Overview

LankaCommerce Cloud uses database routers to ensure that queries and
migrations are directed to the correct PostgreSQL schema. The routing
system maintains data isolation between tenants by enforcing that shared
apps operate in the public schema and tenant apps operate in individual
tenant schemas.

---

## Router Stack

DATABASE_ROUTERS controls the order in which routers are consulted.
LankaCommerce uses two routers, evaluated in order:

| Priority | Router                                  | Purpose                              |
| -------- | --------------------------------------- | ------------------------------------ |
| 1        | apps.tenants.routers.TenantRouter       | Cross-schema relation prevention     |
| 2        | django_tenants.routers.TenantSyncRouter | Migration routing (shared vs tenant) |

Django evaluates routers in order. For each database operation, the first
router to return a non-None value wins. If all routers return None, Django
falls back to default behavior.

---

## TenantSyncRouter (django-tenants built-in)

The TenantSyncRouter is provided by django-tenants and handles migration
routing. It implements only the allow_migrate method.

### Behavior

The router inspects the app label of each model during migrate_schemas:

- If the app is in SHARED_APPS, migrations run in the public schema only
- If the app is in TENANT_APPS, migrations run in each tenant schema only
- Apps in both lists (contenttypes, auth) get tables in both schemas

### How It Works

When manage.py migrate_schemas is executed:

1. django-tenants calls migrate_schemas for the public schema first
2. TenantSyncRouter.allow_migrate returns True for SHARED_APPS, False for others
3. Only SHARED_APPS tables are created in public
4. Then migrate_schemas iterates each tenant schema
5. TenantSyncRouter.allow_migrate returns True for TENANT_APPS, False for others
6. Only TENANT_APPS tables are created in each tenant schema

### Methods

| Method         | Implemented | Behavior                                            |
| -------------- | ----------- | --------------------------------------------------- |
| allow_migrate  | Yes         | Routes migrations to correct schema (shared/tenant) |
| db_for_read    | No          | Falls through to default (handled by search_path)   |
| db_for_write   | No          | Falls through to default (handled by search_path)   |
| allow_relation | No          | Falls through to default                            |

Note: db_for_read and db_for_write are not needed because django-tenants
uses PostgreSQL's search_path mechanism. The middleware sets search_path
to the current tenant's schema, so all queries automatically hit the
correct schema without needing router-level read/write routing.

---

## TenantRouter (LankaCommerce custom)

The TenantRouter is defined in backend/apps/tenants/routers.py and handles
cross-schema relation prevention.

### Purpose

Prevents Django from creating or allowing foreign key relationships between
models in different schema classifications (shared vs tenant). This is
critical for data isolation.

### Methods

| Method         | Behavior                                                  |
| -------------- | --------------------------------------------------------- |
| allow_relation | Blocks relations between shared-only and tenant-only apps |

### Relation Rules

| Source App    | Target App    | Allowed | Reason                          |
| ------------- | ------------- | ------- | ------------------------------- |
| Shared only   | Shared only   | Yes     | Both in public schema           |
| Tenant only   | Tenant only   | Yes     | Both in tenant schema           |
| Shared+Tenant | Any           | Yes     | Dual apps exist in both schemas |
| Any           | Shared+Tenant | Yes     | Dual apps exist in both schemas |
| Shared only   | Tenant only   | No      | Cross-schema FK would break     |
| Tenant only   | Shared only   | No      | Cross-schema FK would break     |

Dual apps are those that appear in both SHARED_APPS and TENANT_APPS
(currently: django.contrib.contenttypes and django.contrib.auth).
Relations involving dual apps are always allowed because the tables
exist in both schemas.

---

## Routing Rules Summary

### Shared Apps (public schema only)

These apps have tables only in the public schema:

- django_tenants — Multi-tenancy infrastructure
- django.contrib.admin — Admin interface
- django.contrib.sessions — Session storage
- django.contrib.messages — Flash messages
- django.contrib.staticfiles — Static file management
- apps.tenants — Tenant and Domain models
- apps.core — Core utilities and base models
- apps.users — User profiles and management
- rest_framework — DRF API framework
- django_filters — Query filtering
- rest_framework_simplejwt — JWT authentication
- drf_spectacular — OpenAPI documentation
- corsheaders — CORS handling
- channels — WebSocket support
- django_celery_beat — Celery beat scheduler
- django_celery_results — Celery results backend

### Tenant Apps (per-tenant schema)

These apps have tables in each tenant schema:

- apps.products — Product catalog
- apps.inventory — Stock and warehouse
- apps.vendors — Supplier management
- apps.sales — Orders, invoicing, POS
- apps.customers — Customer CRM
- apps.hr — Human resources
- apps.accounting — Accounting and finance
- apps.reports — Reports and analytics
- apps.webstore — E-commerce storefront
- apps.integrations — Third-party integrations

### Dual Apps (both schemas)

These apps have tables in both the public and tenant schemas:

- django.contrib.contenttypes — Content type registry per schema
- django.contrib.auth — Users, groups, permissions per schema

---

## Cross-Schema Relations

### Why Cross-Schema FKs Are Prohibited

PostgreSQL foreign keys work within a single schema's search_path. When
django-tenants sets search_path to a tenant schema, FK references to
tables in the public schema would fail because the public schema is not
in the search path.

### Allowed Patterns

- Tenant model A references tenant model B (same schema): allowed
- Shared model A references shared model B (public schema): allowed
- Any model references a dual app model: allowed (tables exist in both)

### Prohibited Patterns

- Tenant model references a shared-only model: prohibited
- Shared-only model references a tenant model: prohibited

### How Violations Are Prevented

1. The TenantRouter.allow_relation method returns False for cross-schema FKs
2. Django will refuse to create the migration if the router blocks it
3. Code review guidelines reinforce the rule
4. The SHARED_APPS and TENANT_APPS classification in database.py serves as
   the single source of truth

---

## Edge Cases

### Unmanaged Models

Models with managed = False in their Meta class are not affected by
migration routing because Django does not create or alter their tables.
However, the allow_relation check still applies to prevent cross-schema
FK declarations in code.

### Third-Party Apps Without Models

Some shared apps (corsheaders, drf_spectacular) have no database models.
They appear in SHARED_APPS for configuration purposes but the router
has no effect on them since there are no migrations to route.

### ContentType and Auth Isolation

contenttypes and auth appear in both SHARED_APPS and TENANT_APPS. This
means each tenant schema has its own ContentType and Permission tables.
This is required by django-tenants for proper GenericForeignKey resolution
and per-tenant permission management.

### Unknown or Unregistered Apps

Apps not listed in either SHARED_APPS or TENANT_APPS default to
shared_only classification. This is a safe fallback because:

- Framework apps not explicitly listed are typically shared
- Unknown apps will not cause cross-schema FK violations with other shared apps
- If an unknown app relates to a tenant-only app, it will be correctly blocked

### model_name=None in allow_migrate

Django sometimes calls allow_migrate with model_name=None (e.g. during
initial migration planning). TenantRouter defers this to TenantSyncRouter
by returning None. TenantSyncRouter handles this case using the app_label
alone to determine routing.

### Same-App Relations

When both objects in an allow_relation call belong to the same app, the
relation is always allowed. Both objects share the same classification,
so the relation stays within a single schema.

### Empty Hints

All router methods accept \*\*hints keyword arguments. TenantRouter ignores
hints entirely. Passing empty hints or hints with arbitrary keys has no
effect on routing behavior.

### db_for_read and db_for_write

TenantRouter returns None for both methods. django-tenants handles read
and write routing via PostgreSQL search_path, not via Django router methods.
The middleware sets search_path before any query executes, making router-level
read/write routing unnecessary.

### Router Evaluation Order

Django evaluates routers in DATABASE_ROUTERS order. TenantRouter is first
to enforce relation rules before TenantSyncRouter processes migrations.
If TenantRouter returns None (for db_for_read, db_for_write, allow_migrate),
Django proceeds to TenantSyncRouter. For allow_relation, TenantRouter
always returns True or False (never None), so TenantSyncRouter is not
consulted for relation decisions.

### Adding New Apps

When adding a new app to the project:

1. Classify it in SHARED_APPS or TENANT_APPS (or both) in database.py
2. The router automatically picks up the classification from settings
3. No changes to routers.py are needed
4. Run the validation script to confirm correct classification

---

## Configuration File

All router settings are in backend/config/settings/database.py.

The custom router is in backend/apps/tenants/routers.py.

---

## Validation Record

Router configuration was validated on 2026-02-16 via Docker.

### Migration Routing Validation

| Category    | Count | Result | Details                                                        |
| ----------- | ----- | ------ | -------------------------------------------------------------- |
| Shared-only | 16    | PASS   | All 16 shared-only apps classified correctly                   |
| Tenant-only | 10    | PASS   | All 10 tenant-only apps classified correctly                   |
| Dual        | 2     | PASS   | contenttypes and auth in both SHARED_APPS/TENANT_APPS          |
| Exclusions  | 26    | PASS   | Shared-only not in TENANT_APPS, tenant-only not in SHARED_APPS |

### Relation Restriction Validation

| Test Case       | Count | Result | Details                                  |
| --------------- | ----- | ------ | ---------------------------------------- |
| Shared ↔ Shared | 3     | PASS   | All allowed (same schema)                |
| Tenant ↔ Tenant | 15    | PASS   | All allowed (same schema)                |
| Dual ↔ Any      | 20    | PASS   | All allowed (tables in both schemas)     |
| Shared ↔ Tenant | 20    | PASS   | All blocked (cross-schema FK prevention) |

Total checks: 121 passed, 0 failed.

Full verification details are in docs/VERIFICATION.md.

---

## Related Documentation

- [Tenant Settings](tenant-settings.md) — All multi-tenancy settings
- [App Classification](app-classification.md) — SHARED vs TENANT app lists
- [Tenant Models](tenant-models.md) — Tenant and Domain model reference
- [Schema Naming](schema-naming.md) — Schema naming conventions
