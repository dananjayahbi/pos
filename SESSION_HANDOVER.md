# Session Handover Document

## Date: 2025-07-22

## Project Context

LankaCommerce Cloud Multi-Tenant SaaS ERP — Phase 02: Database Architecture & Multi-Tenancy, SubPhase-04: Tenant Model & Domain Model.

## Tech Stack

- Django 5.2.11, django-tenants 3.10.0, PostgreSQL 15.16, Python 3.12
- AUTH_USER_MODEL = "platform.PlatformUser"
- TENANT_MODEL = "tenants.Tenant", TENANT_DOMAIN_MODEL = "tenants.Domain"
- Currency: LKR (₨), PRICE_MAX_DIGITS=10, PRICE_DECIMAL_PLACES=2
- Tenant model uses Django default AutoField PK (NOT UUID)
- Tenants app uses flat models.py (NOT models/ package)

## Critical Environment Info

- PgBouncer UNAVAILABLE (port 6432 conflict)
- ALL DB commands must use: `docker compose run --rm --no-deps -e DB_HOST=db -e DB_PORT=5432 --entrypoint python backend ...`
- For manage.py: `docker compose run --rm --no-deps -e DB_HOST=db -e DB_PORT=5432 --entrypoint python backend manage.py <cmd>`
- Validation scripts: create at `backend/scripts/<name>.py`, run via Docker `python -c "import os; os.chdir('/app'); exec(open('scripts/<name>.py').read())"`, delete after
- Docs files on host filesystem only (not Docker-mounted)
- flow.py path: `python E:\My_GitHub_Repos\flow\flow.py`

## Database State

- 3 tenants: public (ID=1, schema=public), test-isolation (ID=2), cmd-test (ID=3)
- Each has 1 primary domain (3 total domains)
- TenantSettings record exists for cmd-test tenant (created by Group-D signal)
- SHARED_APPS includes apps.tenants, apps.platform, apps.core, apps.users
- Use migrate_schemas --shared for public schema migrations

## Current Progress — SubPhase-04 Complete Summary

### All Groups A-F Status

| Group                           | Documents   | Tasks       | Status                      |
| ------------------------------- | ----------- | ----------- | --------------------------- |
| Group-A: Tenant Core Fields     | 3 docs      | Tasks 01-16 | COMPLETE                    |
| Group-B: Tenant Extended Fields | 3 docs      | Tasks 17-30 | COMPLETE                    |
| Group-C: Domain Model           | 3 docs      | Tasks 31-46 | COMPLETE                    |
| Group-D: Tenant Settings        | 2 docs      | Tasks 47-58 | COMPLETE                    |
| Group-E: Tenant Subscription    | 2 docs      | Tasks 59-72 | COMPLETE                    |
| Group-F: Admin & Management     | 2 of 3 docs | Tasks 73-83 | COMPLETE (Doc 03 REMAINING) |

### Validation Results Summary

| Document                     | Tests   |
| ---------------------------- | ------- |
| Group-A Doc 01 (Tasks 01-06) | 23/23   |
| Group-A Doc 02 (Tasks 07-12) | 19/19   |
| Group-A Doc 03 (Tasks 13-16) | 26/26   |
| Group-B Doc 01 (Tasks 17-21) | 47/47   |
| Group-B Doc 02 (Tasks 22-26) | 50/50   |
| Group-B Doc 03 (Tasks 27-30) | 49/49   |
| Group-C Doc 01 (Tasks 31-36) | 32/32   |
| Group-C Doc 02 (Tasks 37-42) | 57/57   |
| Group-C Doc 03 (Tasks 43-46) | 55/55   |
| Group-D Doc 01 (Tasks 47-52) | 54/54   |
| Group-D Doc 02 (Tasks 53-58) | 48/48   |
| Group-E Doc 01 (Tasks 59-65) | 79/79   |
| Group-E Doc 02 (Tasks 66-72) | 77/77   |
| Group-F Doc 01 (Tasks 73-79) | 122/122 |
| Group-F Doc 02 (Tasks 80-83) | 74/74   |

## What Remains — Group-F Doc 03 (Tasks 84-88)

The FINAL document in SubPhase-04:

File: `Document-Series\Phase-02_Database-Architecture-MultiTenancy\SubPhase-04_Tenant-Model-Domain-Model\Group-F_Admin-Management\03_Tasks-84-88_Migrations-Commit.md`

Tasks:

- Task 84: Create Migrations (already done — 10 migrations exist)
- Task 85: Review Migration SQL
- Task 86: Run Shared Migrations (already done — all applied)
- Task 87: Create Test Tenants (3 already exist)
- Task 88: Create Initial Commit

NOTE: Most of these tasks may already be satisfied since migrations 0001-0010 all exist and are applied, and test tenants already exist. The document likely needs review of SQL, verification of existing state, and a git commit.

## Files Modified in SubPhase-04 (not yet committed)

### backend/apps/tenants/models.py (1,372 lines)

- Tenant model: 28 fields (name, slug, schema_name, business_type, industry, business_registration_number, contact_name, contact_email, contact_phone, address_line_1, address_line_2, city, district, province, postal_code, logo, primary_color, secondary_color, language, timezone, paid_until, on_trial, status, onboarding_step, onboarding_completed, schema_version, settings, created_on, updated_on)
- Domain model: 11 fields (domain, tenant, is_primary from DomainMixin + domain_type, is_verified, verified_at, ssl_status, ssl_expires_at, metadata, created_on, updated_on)
- TenantSettings model: 12 fields (tenant OneToOne related_name="tenant_settings", theme_color, invoice_prefix, order_prefix, tax_rate, invoice_footer, receipt_footer, notification_settings, feature_settings, integration_settings, created_on, updated_on)
- TenantSubscription model: 13 fields (tenant FK related_name="subscriptions", plan FK to platform.SubscriptionPlan related_name="tenant_subscriptions", status, billing_cycle, started_at, expires_at, trial_ends_at, next_billing_date, amount, payment_method, is_auto_renew, created_on, updated_on)
- Module constants: TENANT*STATUS*_, BUSINESS*TYPE_CHOICES, INDUSTRY_CHOICES, PROVINCE_CHOICES, LANGUAGE_CHOICES, TIMEZONE_CHOICES, SUBSCRIPTION_STATUS*_, BILLING*CYCLE*\*
- Validators: slug_validator, brn_validator, phone_validator, postal_code_validator, hex_color_validator
- Functions: tenant_logo_upload_path, default_notification_settings, default_feature_settings, default_integration_settings

### backend/apps/tenants/managers.py (526 lines)

- TenantQuerySet: 12 methods (active, suspended, archived, not_archived, on_trial, not_on_trial, paid, expired, onboarded, needs_onboarding, business, public_only)
- TenantManager: wraps TenantQuerySet, 12 shortcuts
- DomainQuerySet: 12 methods (platform, custom, verified, unverified, needs_verification, ssl_active, ssl_expiring_soon, ssl_expired, ssl_pending, active_domains, primary, for_tenant)
- DomainManager: wraps DomainQuerySet, 12 shortcuts
- SubscriptionQuerySet: 15 methods (active, trial, active_or_trial, expired, cancelled, suspended, monthly, annual, auto_renew, no_auto_renew, expiring_soon, trial_ending_soon, billing_due, for_tenant, current_for_tenant)
- SubscriptionManager: wraps SubscriptionQuerySet, 15 shortcuts

### backend/apps/tenants/admin.py (585 lines)

- TenantAdmin: 8 list_display, 6 list_filter, 6 search_fields, 3 readonly_fields, 12 fieldsets, 3 inlines, 3 actions
- DomainAdmin: 6 list_display, 4 list_filter, 3 search_fields, 4 readonly_fields, 5 fieldsets, 1 action
- TenantSubscriptionAdmin: 9 list_display, 3 list_filter, 3 search_fields, 2 readonly_fields, 4 fieldsets
- DomainInline (TabularInline): 8 fields, 3 readonly
- TenantSettingsInline (StackedInline): 11 fields, 2 readonly, max_num=1, can_delete=False
- TenantSubscriptionInline (TabularInline): 11 fields, 1 readonly
- Actions: verify_domains, suspend_tenants, activate_tenants, export_tenants_csv

### backend/apps/tenants/signals.py (53 lines, NEW)

- create_tenant_settings: post_save receiver on Tenant, auto-creates TenantSettings on first save

### backend/apps/tenants/apps.py (24 lines)

- TenantsConfig with ready() method importing signals

### Migrations (10 total, all applied)

- 0001_initial.py — Original Tenant/Domain
- 0002_add_onboarding_schema_metadata.py — onboarding_step, onboarding_completed, schema_version, 2 indexes
- 0003_add_business_info_contact.py — business_type, industry, BRN, contact fields
- 0004_add_address_fields.py — address fields + altered contact_phone
- 0005_add_branding_locale.py — logo, primary_color, secondary_color, language, timezone
- 0006_add_domain_type_ssl_meta.py — domain_type, verification, SSL, metadata, timestamps, 2 indexes
- 0007_add_tenant_settings.py — TenantSettings model creation
- 0008_add_settings_text_json.py — footer text fields + 3 JSON settings fields
- 0009_add_tenant_subscription.py — TenantSubscription model creation
- 0010_add_billing_fields.py — trial_ends_at, next_billing_date, amount, payment_method, is_auto_renew

### docs/VERIFICATION.md (~6000+ lines)

- Contains all verification records from SubPhase-03 through SubPhase-04 Group-F Doc 02

## Git Status

- SubPhase-03: FULLY COMMITTED (commit 0742eba)
- SubPhase-04 Groups A-F (Docs 01-02): ALL COMPLETE, NOT YET COMMITTED
- A commit should happen after Group-F Doc 03 (Task 88)

## Key Gotchas for Next Session

1. Field name is `business_registration_number` (NOT `brn`) — the property `has_brn` exists but the field is the full name
2. Field names are `address_line_1` and `address_line_2` (with underscores before the number)
3. TenantSettings.tenant has related_name="tenant_settings" (NOT "settings") because Tenant model has a `settings` JSONField
4. SubscriptionPlan is at `platform.SubscriptionPlan` with UUID primary key
5. Phone validator pattern: `^(\+94|0)[\s-]?\d{2}[\s-]?\d{3}[\s-]?\d{4}$`
6. Postal code validator: `^\d{5}$`
7. SAVEPOINT commands don't work in Docker without explicit transaction blocks — use pg_indexes check instead
8. `timezone.timedelta` doesn't exist — use `from datetime import timedelta`
9. Always delete validation scripts after running them
10. No fenced code blocks in documentation files
