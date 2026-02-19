# Session Handover Document

> **Created:** 2025-07-23
> **Purpose:** Context transfer for next AI coding session
> **Project:** LankaCommerce Cloud - Multi-Tenant SaaS ERP
> **Delete after use:** Yes (placed in project root for easy cleanup)

---

## 1. Overall Progress Summary

### Document-Series Phase-02, SubPhase-03: Public Schema Design

| Group | Name                              | Tasks | Status      | Validation |
| ----- | --------------------------------- | ----- | ----------- | ---------- |
| A     | Public Schema Planning            | 01-12 | ✅ COMPLETE | All passed |
| B     | Subscription Plans Model          | 13-28 | ✅ COMPLETE | 153/153    |
| C     | Platform Settings Model           | 29-42 | ✅ COMPLETE | 146/146    |
| D     | Platform Users & Super Admin      | 43-58 | ✅ COMPLETE | 185/185    |
| E     | Feature Flags System (Docs 01-02) | 59-68 | ✅ COMPLETE | 142/142    |
| E     | Feature Flags System (Doc 03)     | 69-72 | ✅ COMPLETE | 65/65      |
| F     | Platform Audit & Billing (Doc 01) | 73-78 | ✅ COMPLETE | 93/93      |
| F     | Platform Audit & Billing (Doc 02) | 79-84 | ✅ COMPLETE | 126/126    |
| G     | Migration & Verification (Doc 01) | 85-88 | ✅ COMPLETE | 92/92      |
| G     | Migration & Verification (Doc 02) | 89-92 | ✅ COMPLETE | 14/14      |

### Next Task

**SubPhase-03 is COMPLETE.** All 92 tasks (Groups A through G) have been implemented and validated.

Next step: Create the final commit for SubPhase-03 (Public Schema Design) and proceed to SubPhase-04 or the next phase as defined in the Document-Series.

---

## 2. Git State

- **Branch:** main
- **Ahead of remote:** 4 commits (unpushed)
- **SubPhase-02** (django-tenants) is committed as `feat: install and configure django-tenants`
- **SubPhase-03** changes are ALL UNCOMMITTED

### Uncommitted Changes

**Modified files:**

- backend/config/settings/base.py
- backend/config/settings/database.py
- docs/VERIFICATION.md
- docs/index.md

**New (untracked) directories:**

- backend/apps/platform/ (entire app)
- docs/database/naming-conventions.md
- docs/database/public-schema-erd.md
- docs/saas/ (subscription-plans.md, feature-flags.md)
- docs/users/ (user-hierarchy.md, role-permissions.md)

---

## 3. Technical Stack

| Component               | Version/Value                                                                    |
| ----------------------- | -------------------------------------------------------------------------------- |
| Django                  | 5.2.11                                                                           |
| django-tenants          | 3.10.0                                                                           |
| PostgreSQL              | 15.16                                                                            |
| Python                  | 3.12                                                                             |
| AUTH_USER_MODEL         | "platform.PlatformUser"                                                          |
| AUTHENTICATION_BACKENDS | ["apps.platform.backends.EmailBackend"]                                          |
| DATABASE_ROUTERS        | ["apps.tenants.routers.TenantRouter", "django_tenants.routers.TenantSyncRouter"] |
| SHARED_APPS             | 19 apps (includes apps.platform, apps.users)                                     |
| TENANT_APPS             | 12 apps                                                                          |
| Tenants in DB           | public (ID=1), test-isolation (ID=2), cmd-test (ID=3)                            |

### Docker Commands

**CRITICAL:** PgBouncer is UNAVAILABLE (port 6432 binding conflict). ALL DB commands must use:

```
docker compose run --rm --no-deps -e DB_HOST=db -e DB_PORT=5432 --entrypoint python backend -c "<command>"
```

For validation scripts:

```
docker compose run --rm --no-deps -e DB_HOST=db -e DB_PORT=5432 --entrypoint python backend -c "exec(open('scripts/<script_name>.py').read())"
```

---

## 4. File Inventory — Platform App

### Models (backend/apps/platform/models/)

| File            | Model/Purpose                                           | Mixins Used                           |
| --------------- | ------------------------------------------------------- | ------------------------------------- |
| mixins.py       | UUIDMixin, TimestampMixin, StatusMixin, SoftDeleteMixin | Abstract bases                        |
| subscription.py | SubscriptionPlan — SaaS subscription tiers              | UUID+Timestamp+Status+SoftDelete      |
| settings.py     | PlatformSetting — singleton config with caching         | UUID+Timestamp only                   |
| user.py         | PlatformUser — AUTH_USER_MODEL with roles               | UUID+Timestamp+AbstractBaseUser       |
| managers.py     | PlatformUserManager — create_user/create_superuser      | —                                     |
| features.py     | FeatureFlag — global feature toggles                    | UUID+Timestamp+Status (NO SoftDelete) |
| overrides.py    | TenantFeatureOverride — per-tenant flag overrides       | UUID+Timestamp only                   |
| audit.py        | AuditLog — immutable audit log for platform actions     | UUID+Timestamp (NO Status/SoftDelete) |
| billing.py      | BillingRecord — tenant subscription billing records     | UUID+Timestamp+Status+SoftDelete      |
| **init**.py     | Package init — exports all models + constants           | —                                     |

### Admin (backend/apps/platform/admin.py — ~831 lines)

5 base admin classes:

- PlatformModelAdmin — base with UUID/timestamp readonly
- StatusModelAdmin — adds is_active/deactivated_on
- SoftDeleteModelAdmin — adds is_deleted/deleted_on
- FullPlatformModelAdmin — both status + soft delete
- ReadOnlyPlatformAdmin — immutable records

Registered model admins:

- SubscriptionPlanAdmin (extends FullPlatformModelAdmin)
- FeatureFlagAdmin (extends StatusModelAdmin)
- TenantFeatureOverrideAdmin (extends PlatformModelAdmin)
- AuditLogAdmin (extends ReadOnlyPlatformAdmin)
- BillingRecordAdmin (extends FullPlatformModelAdmin)
- PlatformSettingAdmin (extends PlatformModelAdmin, singleton guard)
- PlatformUserAdmin (extends Django's BaseUserAdmin)

### Auth (backend/apps/platform/backends.py)

- EmailBackend — case-insensitive email authentication with timing attack prevention

### Management Commands (backend/apps/platform/management/commands/)

- create_platform_admin.py — Creates non-superuser platform staff (platform_admin/support/viewer roles)

### Utilities (backend/apps/platform/utils/)

- settings.py — get_platform_settings, get_setting, invalidate_settings_cache, is_maintenance_mode, is_feature_enabled
- features.py — is_flag_enabled, get_tenant_flags, invalidate_feature_cache, invalidate_all_feature_caches

### Fixtures (backend/apps/platform/fixtures/)

- subscription_plans.json — 4 plans (Free, Starter, Pro, Enterprise) — LOADED
- feature_flags.json — 8 flags across 4 modules (billing, inventory, reports, webstore) — LOADED

### Migrations (backend/apps/platform/migrations/)

- 0001_initial_platform_models.py — 7 models, 24 custom indexes, 5 FKs — APPLIED

---

## 5. Key Model Details

### PlatformUser Roles & Permissions

| Role           | Value          | can_manage_tenants | can_manage_users | can_manage_billing | can_view_audit_logs |
| -------------- | -------------- | ------------------ | ---------------- | ------------------ | ------------------- |
| Super Admin    | super_admin    | ✅                 | ✅               | ✅                 | ✅                  |
| Platform Admin | platform_admin | ✅                 | ❌               | ❌                 | ✅                  |
| Support        | support        | ❌                 | ❌               | ❌                 | ✅                  |
| Viewer         | viewer         | ❌                 | ❌               | ❌                 | ❌                  |

### FeatureFlag Fields

- key (CharField, unique, max 100, snake_case with module prefix)
- name (CharField, max 200)
- description (TextField, max 500, blank)
- rollout_percentage (IntegerField, 0-100, validators, default 0)
- is_active (from StatusMixin, default True)
- is_public (BooleanField, default False)
- Properties: is_fully_rolled_out, is_disabled, rollout_display

### TenantFeatureOverride Fields

- tenant (FK to tenants.Tenant, CASCADE)
- feature_flag (FK to FeatureFlag, CASCADE)
- is_enabled (BooleanField — force-enable/force-disable)
- reason (TextField, max 500, blank)
- unique_together: (tenant, feature_flag)

### Feature Flag Resolution Order

1. Check TenantFeatureOverride for tenant+flag pair
2. If override exists, use is_enabled (authoritative)
3. If no override, use global FeatureFlag state
4. Default: disabled

### Caching Strategy

- Cache key: feature_flags:{tenant_id}
- TTL: 3600 seconds (1 hour)
- Flag changes → invalidate ALL tenant caches
- Override changes → invalidate only affected tenant's cache

---

## 6. Settings Configuration (base.py)

- AUTH_USER_MODEL = "platform.PlatformUser" (~line 300)
- AUTHENTICATION_BACKENDS = ["apps.platform.backends.EmailBackend"] (~lines 305-308)
- 4 AUTH_PASSWORD_VALIDATORS (min_length=8)
- AuthenticationMiddleware in MIDDLEWARE (line 121)
- No CACHES in base.py (defined in production.py with Redis, test.py with LocMem)

---

## 7. Documentation Files

| File                                | Content                                                             |
| ----------------------------------- | ------------------------------------------------------------------- |
| docs/saas/subscription-plans.md     | Subscription plan tiers documentation                               |
| docs/saas/feature-flags.md          | Feature flags, tenant overrides, resolution order, caching strategy |
| docs/users/user-hierarchy.md        | Platform vs tenant users, auth config, roles, management commands   |
| docs/users/role-permissions.md      | Role definitions, permission matrix, enforcement strategy           |
| docs/database/naming-conventions.md | Database naming conventions                                         |
| docs/database/public-schema-erd.md  | Public schema ERD                                                   |
| docs/index.md                       | Main docs index with links to all above                             |
| docs/VERIFICATION.md                | Complete verification record (~3600+ lines)                         |

---

## 8. Standing Instructions for Next Session

1. **Read the task document first** — each doc in Document-Series has specific tasks and verification checklists
2. **Use subagents** to gather codebase context before implementing (manages context window)
3. **Update todo list** for each task set
4. **No fenced code blocks in documentation** — docs use plain prose only
5. **Validation pattern:** Create temp script at `backend/scripts/validate_*.py`, run via Docker exec, delete after
6. **Validation scripts must use os.getcwd() not **file\***\* — exec() does not define **file\*\*
7. **Host doc checks** — docs/ directory is not mounted in Docker, verify docs on host via PowerShell
8. **VERIFICATION.md** — update after each document's validation passes
9. **When replacing in VERIFICATION.md** — use enough unique context to avoid multiple matches
10. **flow.py** — run `python E:\My_GitHub_Repos\flow\flow.py` after every task completion for user review
11. **Add flow.py to task list** — always include it as a todo item

---

## 9. Next Steps (in order)

1. **SubPhase-03 is COMPLETE** — All Groups A-G (Tasks 01-92) implemented and validated
2. **Final commit** for SubPhase-03 Public Schema Design changes
3. **Proceed to next SubPhase or Phase** as defined in the Document-Series

---

## 10. Known Issues / Gotchas

- **PgBouncer port conflict:** Always use `--no-deps -e DB_HOST=db -e DB_PORT=5432` for Docker commands
- **ReadOnlyPlatformAdmin:** Had a crash with **dict** check — was fixed
- **CACHES not in base.py:** Only in production.py (Redis) and test.py (LocMem). The `django.core.cache.cache` default backend works in dev with Django's default (locmem) cache
- **3 tenants exist in DB:** public, test-isolation, cmd-test — created during earlier validation
- **Feature flag admin already has FeatureFlagAdmin AND TenantFeatureOverrideAdmin** — both registered
- **The is_feature_enabled in utils/settings.py** is for PlatformSetting toggles (enable_webstore etc.), NOT for FeatureFlag model. The FeatureFlag resolution is in utils/features.py (is_flag_enabled)
