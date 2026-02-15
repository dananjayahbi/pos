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
- Local integrations (e.g., PayHere, Domex/Koombiyo) _(planned)_
- Sinhala/Singlish-aware UX and search _(planned)_

## Features

- **Multi-tenant SaaS** foundation
- **POS**: sales, receipts, barcode scanning flows _(planned)_
- **Webstore**: catalog, cart, checkout _(planned)_
- **Inventory**: stock, locations, low-stock alerts _(planned)_
- **Financial module**: invoicing, accounting basics _(planned)_
- **AI-assisted capabilities** _(planned)_

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
- GitHub Actions _(planned)_

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
- [Branching Strategy](docs/BRANCHING.md)
- [Branch Protection & Merge Rules](docs/BRANCH_PROTECTION.md)
- [Commit Conventions](docs/COMMITS.md)
- [Code Review Guidelines](docs/CODE_REVIEW.md)
- [Changelog](CHANGELOG.md)

## Community

- [Contributing Guide](CONTRIBUTING.md) — how to contribute code, docs, and translations
- [Code of Conduct](CODE_OF_CONDUCT.md) — community standards and expectations
- [Security Policy](SECURITY.md) — how to report vulnerabilities privately

## Contributing

Contributions are welcome — please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

We follow:

- **Conventional Commits** — see [COMMITS.md](docs/COMMITS.md)
- **Git Flow** branching — see [BRANCHING.md](docs/BRANCHING.md)
- **Code Review** standards — see [CODE_REVIEW.md](docs/CODE_REVIEW.md)

## License

MIT — see `LICENSE`.

---

© 2026 LankaCommerce Cloud Contributors • Contact: `dev@lankacommerce.lk` (placeholder)
