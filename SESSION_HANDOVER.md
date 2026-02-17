# Session Handover — LankaCommerce Cloud

> Continue from here in the next chat session.

---

## Project Summary

- **Project:** LankaCommerce Cloud (LCC) — Multi-tenant SaaS ERP for Sri Lankan SMEs
- **Repository:** e:\work_git_repos\pos\
- **Branch:** main
- **Latest Commit:** 9b1dfd3 — feat: configure postgresql for multi-tenancy (SubPhase-01)

---

## Tech Stack

- **Backend:** Django 5.2.11, DRF 3.16.1, django-tenants 3.10.0, psycopg[binary] 3.3.2, Celery 5.6.2
- **Database:** PostgreSQL 15.16 with PgBouncer connection pooling
- **Frontend:** Next.js, TypeScript, Tailwind CSS, pnpm
- **Infrastructure:** Docker Compose (8 services: backend, frontend, db, pgbouncer, redis, celery-worker, celery-beat, flower)

---

## Current Position

- **Phase:** 02 — Database Architecture and Multi-Tenancy
- **SubPhase:** 02 — Django-Tenants Installation (86 total tasks across 6 groups)
- **Document-Series Path:** Document-Series\Phase-02_Database-Architecture-MultiTenancy\SubPhase-02_Django-Tenants-Installation\

### Progress

| Group                      | Document       | Tasks | Status      |
| -------------------------- | -------------- | ----- | ----------- |
| A — Package Installation   | 01_Tasks-01-05 | 01-05 | DONE        |
| A — Package Installation   | 02_Tasks-06-10 | 06-10 | DONE        |
| B — Database Settings      | 01_Tasks-11-16 | 11-16 | DONE        |
| B — Database Settings      | 02_Tasks-17-21 | 17-21 | DONE        |
| B — Database Settings      | 03_Tasks-22-26 | 22-26 | DONE        |
| C — App Classification     | 01_Tasks-27-32 | 27-32 | DONE        |
| C — App Classification     | 02_Tasks-33-37 | 33-37 | DONE        |
| C — App Classification     | 03_Tasks-38-42 | 38-42 | NEXT        |
| D — Model Configuration    | 01 to 03       | 43-56 | Not Started |
| E — Database Router        | 01 to 03       | 57-68 | Not Started |
| F — Migration Verification | 01 to 03       | 69-86 | Not Started |

### Next Task

Read and implement: Group-C_App-Classification-SHARED-TENANT/03_Tasks-38-42_Registry-Verification.md

Tasks 38-42 cover: App registry verification, shared/tenant migration validation, auth per-tenant decision documentation, classification verification record.

After Group-C Document 03, proceed to Group-D (Model Configuration, Tasks 43-56).

---

## Key Files and Their Current State

### Settings Architecture

- **backend/config/settings/database.py** — Central multi-tenancy config. Contains:
  - TENANT_MODEL, TENANT_DOMAIN_MODEL, DATABASE_ROUTERS
  - PUBLIC_SCHEMA_NAME, SHOW_PUBLIC_IF_NO_TENANT_FOUND
  - BASE_TENANT_DOMAIN (env-configurable), TENANT_SCHEMA_PREFIX
  - AUTO_CREATE_SCHEMA=True, AUTO_DROP_SCHEMA=False
  - MULTITENANT_RELATIVE_MEDIA_ROOT
  - SHARED_APPS (18 apps — finalized)
  - TENANT_APPS (12 apps — finalized with 10 business modules)
  - INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS] (28 apps total)

- **backend/config/settings/base.py** — Core Django settings. DJANGO_APPS/THIRD_PARTY_APPS/LOCAL_APPS kept as reference only. INSTALLED_APPS is now defined in database.py via the import: from config.settings.database import \* (at line ~287). TenantMainMiddleware still commented out. STORAGES has TenantFileSystemStorage for default.

- **backend/config/settings/local.py** — DB_ENGINE defaults to django_tenants.postgresql_backend, DB_HOST=pgbouncer, DB_PORT=6432

- **backend/config/settings/production.py** — DB_ENGINE=django_tenants.postgresql_backend, sslmode=require

### Environment Files

- **.env.docker** — DB_HOST=pgbouncer, DB_PORT=6432, DB_PASSWORD=dev_password_change_me, DB_ENGINE=django_tenants.postgresql_backend, DATABASE_URL uses pgbouncer:6432, BASE_TENANT_DOMAIN=localhost
- **.env.docker.example** — Same structure as .env.docker
- **backend/.env.example** — DB_ENGINE and BASE_TENANT_DOMAIN defaults

### Docker Notes

- PgBouncer host port mapped via PGBOUNCER_HOST_PORT env var (default 6432, may need different port if Hyper-V excludes it)
- Use --no-deps --entrypoint python to bypass Redis dependency when validating settings
- Build command: docker compose build backend
- Validation command: docker compose run --rm --no-deps --entrypoint python backend -c "..."

### Documentation

- **docs/database/tenant-settings.md** — Comprehensive tenant settings reference
- **docs/database/app-classification.md** — SHARED vs TENANT classification guide (NEW)
- **docs/database/schema-naming.md** — Schema naming conventions
- **docs/index.md** — Central docs hub with links to all database docs
- **docs/VERIFICATION.md** — Verification records for all completed tasks through Group-C Document 02

---

## Uncommitted Changes

All work since commit 9b1dfd3 is uncommitted. Key modified/new files:

- backend/config/settings/database.py (major — all tenant settings, SHARED_APPS, TENANT_APPS, INSTALLED_APPS)
- backend/config/settings/base.py (INSTALLED_APPS moved to database.py, STORAGES updated)
- backend/config/settings/local.py (DB_ENGINE default)
- backend/config/settings/production.py (DB_ENGINE)
- .env.docker, .env.docker.example, backend/.env.example (DB credentials and engine fixes)
- docker-compose.yml (pgbouncer port mapping)
- docker/backend/Dockerfile.dev (build updates)
- docker/postgres/init/01-init.sql (idempotent init)
- docs/database/tenant-settings.md (NEW)
- docs/database/app-classification.md (NEW)
- docs/index.md (new links)
- docs/VERIFICATION.md (all verification records)
- backend/entrypoint.sh (Redis wait logic)
- .gitignore (updates)

These will be committed as a single SubPhase-02 commit when all 86 tasks are complete.

---

## Standing Instructions

1. Read the next document and implement its tasks
2. Update todo list for listed tasks
3. Follow currently implemented folder structure
4. Use subagents to manage context window
5. Add flow.py task to every todo list
6. No fenced code blocks in documentation files
7. Run flow.py after each document completion: python E:\My_GitHub_Repos\flow\flow.py
8. Commitlint requires fully lowercase commit subjects

---

## Database Credentials (Development)

- PostgreSQL superuser: postgres / Indusara2
- Application user: lcc_user / dev_password_change_me
- Database name: lankacommerce
- PgBouncer connection: pgbouncer:6432 (inside Docker), localhost:PGBOUNCER_HOST_PORT (from host)
