# LankaCommerce Cloud (LCC)

> **Sri Lanka-first multi-tenant POS + ERP + Webstore platform** (LKR-ready, Sinhala/Singlish-friendly) 🇱🇰

<!-- Logo placeholder: add later -->
<!-- ![LankaCommerce Cloud Logo](docs/assets/logo.svg) -->

<!-- Badges (placeholders) -->
![Build](https://img.shields.io/badge/build-TBD-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-0.0.1-informational)

## Overview

LankaCommerce Cloud (LCC) is a modern, cloud-native SaaS platform designed for Sri Lankan SMEs.
It brings **POS**, **ERP**, and a **customer-facing webstore** into one multi-tenant system.

Key focus areas:
- Multi-tenant architecture (secure tenant isolation)
- Sri Lanka localization (LKR, Asia/Colombo)
- Local integrations (e.g., PayHere, Domex/Koombiyo) *(planned)*
- Sinhala/Singlish-aware UX and search *(planned)*

## Features

- **Multi-tenant SaaS** foundation
- **POS**: sales, receipts, barcode scanning flows *(planned)*
- **Webstore**: catalog, cart, checkout *(planned)*
- **Inventory**: stock, locations, low-stock alerts *(planned)*
- **Financial module**: invoicing, accounting basics *(planned)*
- **AI-assisted capabilities** *(planned)*

## Tech stack

### Backend
- Django (multi-tenant via `django-tenants`)
- PostgreSQL
- Redis + Celery

### Frontend
- Next.js
- TypeScript
- Tailwind CSS

### Infrastructure
- Docker / Docker Compose
- GitHub Actions *(planned)*

## Prerequisites

- Git
- Docker Desktop
- Python (recommended: 3.12+)
- Node.js (recommended: 20 LTS)

## Quick start (development)

> The full Docker/monorepo scaffolding is created in subsequent Phase-01 tasks. This section will become executable once those files land.

High-level flow:
1. Clone the repository
2. Copy environment variables from `.env.example` (when available)
3. Start the dev stack with Docker Compose
4. Open the apps in your browser

Expected dev URLs (to be finalized):
- Backend API: `http://localhost:8000/`
- Frontend: `http://localhost:3000/`

Timezone note: `Asia/Colombo`

## Project structure

Current:
- `Document-Series/` — AI-agent-driven implementation plan (phases + subphases)

Planned (created in upcoming tasks):
- `backend/` — Django API + tenant services
- `frontend/` — Next.js ERP dashboard + webstore
- `infra/` — docker, scripts, tooling

## Development

Common commands (to be added with tooling in later tasks):
- `docker compose up -d`
- `docker compose down`
- Backend tests (pytest)
- Frontend lint/test/build

## Documentation

- Master index: `Document-Series/00_PHASES_SUMMARY.md`

## Contributing

Contributions are welcome — please read `CONTRIBUTING.md` first.

## License

MIT — see `LICENSE`.

---

© 2026 LankaCommerce Cloud Contributors • Contact: `dev@lankacommerce.lk` (placeholder)
