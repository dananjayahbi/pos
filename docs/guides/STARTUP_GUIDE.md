# LankaCommerce POS-ERP — System Startup Guide

This guide explains how to start the full application stack and access it in a browser.

---

## Prerequisites

- **WSL 2** installed and running
- **Docker** installed inside WSL (no Docker Desktop required)
- All environment files present (`.env.docker`, `docker-compose.override.yml`)

---

## Step-by-Step: Starting the System

### 1. Open a terminal (Git Bash or PowerShell on Windows)

All Docker commands run from Git Bash or any terminal in the project root. The repo path on this machine is `/e/work_git_repos/pos`.

```bash
cd /e/work_git_repos/pos && docker compose <command>
```

---

### 2. Start all services

```bash
cd /e/work_git_repos/pos && docker compose up -d
```

This starts:
| Service | Role |
|---|---|
| `lcc-postgres` | PostgreSQL 15 database |
| `lcc-pgbouncer` | Connection pooler (port 6432) |
| `lcc-redis` | Cache & message broker |
| `lcc-backend` | Django REST API (port **8002**) |
| `lcc-celery-worker` | Async task worker |
| `lcc-celery-beat` | Scheduled task runner |
| `lcc-flower` | Celery monitoring UI |
| `lcc-frontend` | Next.js frontend (port **3002**) |

---

### 3. Wait for services to become healthy (~30–60 seconds)

```bash
cd /e/work_git_repos/pos && docker compose ps
```

Wait until you see `(healthy)` next to `lcc-backend` and `lcc-frontend`. Example output:

```
NAME                STATUS
lcc-backend         Up 2 minutes (healthy)
lcc-celery-beat     Up 2 minutes
lcc-celery-worker   Up 2 minutes (healthy)
lcc-flower          Up 2 minutes
lcc-frontend        Up 2 minutes (healthy)
lcc-pgbouncer       Up 2 minutes (healthy)
lcc-postgres        Up 2 minutes (healthy)
lcc-redis           Up 2 minutes (healthy)
```

> **Note:** The frontend takes 30–90 seconds to compile on first start.

---

### 4. Open the application in your browser

| URL                                      | Purpose                          |
| ---------------------------------------- | -------------------------------- |
| **http://localhost:3002/login**          | Tenant / business login ✅       |
| **http://localhost:3002/platform/login** | Platform admin login ✅          |
| http://localhost:3002/                   | Storefront (public webstore)     |
| http://localhost:3002/dashboard          | ERP Dashboard (after tenant login) |
| http://localhost:3002/platform/dashboard | Platform admin dashboard (after platform login) |
| http://localhost:8002/api/v1/            | Backend REST API                 |
| http://localhost:8002/admin/             | Django admin panel               |

---

### 5. Log in

> **Important:** There are two separate login pages for two different user types.

#### Platform Admin (super-admin / platform staff)

Platform admins manage the SaaS platform itself — tenants, subscriptions, billing. They log in at a **separate URL**:

| Field        | Value                              |
| ------------ | ---------------------------------- |
| **URL**      | `http://localhost:3002/platform/login` |
| **Email**    | `admin@lcc.lk`                     |
| **Password** | `Admin1234x`                       |

After login → redirected to **http://localhost:3002/platform/dashboard**.

#### Tenant Admin (business owner / staff)

Tenant users manage their own store — inventory, sales, employees. They log in at:

| Field        | Value                          |
| ------------ | ------------------------------ |
| **URL**      | `http://localhost:3002/login`  |
| **Email**    | *(registered tenant user)*     |
| **Password** | *(set during registration)*    |

After login → redirected to **http://localhost:3002/dashboard**.

---

## Stopping the System

```bash
cd /e/work_git_repos/pos && docker compose down
```

To stop **without** losing database data, use the above. To also delete volumes (full reset):

```bash
cd /e/work_git_repos/pos && docker compose down -v
```

---

## Troubleshooting

### Frontend shows 500 error on first start

The Next.js dev server compiles on first request. Wait 30–60 seconds and refresh.

### Login shows "An unexpected error occurred"

This was caused by a CORS misconfiguration. The backend must:

1. Have `CORS_ALLOW_ALL_ORIGINS = False` in `local.py` (cannot be `True` when `CORS_ALLOW_CREDENTIALS=True`)
2. Allow custom headers `x-request-id` and `x-tenant-id` via `CORS_ALLOW_HEADERS` in `base.py`
3. Have `CORS_ALLOWED_ORIGINS=http://localhost:3002` in the environment (see `.env.docker`)

Tenant login page is at **`http://localhost:3002/login`**. Platform admin login is at **`http://localhost:3002/platform/login`**.

### Platform admin credentials not working at `/login`

The tenant login (`/login`) and platform admin login (`/platform/login`) are **completely separate**.
`admin@lcc.lk` is a **Platform user** — it only works at `http://localhost:3002/platform/login`.
Logging in at `/login` will fail because that endpoint queries tenant users, not platform users.

### Sidebar only shows "Dashboard" after login

The backend login response doesn't include `role` or `permissions`. The frontend maps `isStaff: true` → `role: "admin"` and `permissions: ["*:*"]`. If you see only Dashboard in the sidebar, clear localStorage and log in again:

1. Open browser DevTools → Application → Local Storage → clear all `lcc-*` keys
2. Navigate to `http://localhost:3002/login` and log in

### Hot reload code changes not taking effect

Hot reload uses file-system polling (required for Windows + Docker WSL2). If changes don't appear after ~10 seconds:

```bash
cd /e/work_git_repos/pos && docker compose restart frontend
```

Wait ~30 seconds for Next.js to recompile, then refresh.

### pgbouncer crash loop (stale PID)

This is automatically handled by the startup command in `docker-compose.yml` (removes stale pidfile before starting). If pgbouncer is still crashing:

```bash
cd /e/work_git_repos/pos && docker compose stop pgbouncer && docker compose rm -f pgbouncer && docker compose up -d pgbouncer
```

Then restart the backend to reconnect:

```bash
cd /e/work_git_repos/pos && docker compose restart backend
```

### Backend cannot connect to database

```bash
cd /e/work_git_repos/pos && docker compose restart backend
```

### Check logs for a specific service

```bash
cd /e/work_git_repos/pos && docker compose logs <service-name> --tail=50
```

Replace `<service-name>` with: `frontend`, `backend`, `pgbouncer`, `postgres`, `redis`, etc.

---

## Checking System Health

```bash
# All services status
cd /e/work_git_repos/pos && docker compose ps

# Frontend health API
curl -s http://localhost:3002/api/health

# Backend health
curl -s http://localhost:8002/api/v1/
```

---

## Architecture Notes

- **Backend** is volume-mounted — code changes apply immediately without rebuild
- **Frontend** is volume-mounted — code changes apply immediately (Next.js hot reload with polling)
- **Database URL**: `postgres://lcc_user:dev_password_change_me@pgbouncer:6432/lankacommerce`
- **Settings module**: `config.settings.local` (inside container)
- **Auth model**: `platform.PlatformUser` (email-based login, not username)
- **CORS**: `CORS_ALLOW_ALL_ORIGINS` must be `False`; allowed origins listed in `CORS_ALLOWED_ORIGINS` env var
- **Custom CORS headers**: `x-request-id` and `x-tenant-id` are allowed via `CORS_ALLOW_HEADERS` in `base.py`
- **Two auth systems**: Platform admin uses `/api/v1/platform/auth/login/` (returns `role`/`is_super_admin`); Tenant users use `/api/v1/auth/login/` (returns `isStaff`/`permissions`)
- **Axios client**: Uses `withCredentials: true`; custom headers require explicit CORS allow-list on backend

---

## Route Reference

### Tenant (Business) Routes

| Route                 | Description                  |
| --------------------- | ---------------------------- |
| `/login`              | Tenant login page            |
| `/register`           | Business registration        |
| `/dashboard`          | ERP dashboard home           |
| `/inventory/products` | Products list                |
| `/sales/orders`       | Sales orders                 |
| `/purchasing/orders`  | Purchase orders              |
| `/accounting`         | Accounting module            |
| `/hr/employees`       | HR — employees               |
| `/settings`           | System settings              |
| `/`                   | Storefront (public webstore) |
| `/shop`               | Shop/product listing         |
| `/account/dashboard`  | Customer portal              |

### Platform Admin Routes

| Route                    | Description                          |
| ------------------------ | ------------------------------------ |
| `/platform/login`        | Platform admin login page            |
| `/platform/dashboard`    | Platform dashboard (tenant stats)    |
| `/platform/tenants`      | Manage all tenants (suspend/reactivate) |
| `/platform/staff`        | Manage platform staff accounts       |
| `/platform/billing`      | Subscription plan management         |
