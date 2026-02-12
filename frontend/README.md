# LankaCommerce Cloud — Frontend

> **Status:** Scaffold — actual Next.js setup will happen in **SubPhase-03: Frontend Project Initialization**.

## Overview

The LankaCommerce Cloud frontend is a modern, multi-tenant web application built with Next.js 14+ (App Router). It provides:

- **ERP Dashboard** — inventory, sales, purchasing, accounting, HR modules
- **POS Interface** — point-of-sale with offline support
- **Webstore / E-Commerce** — customer-facing storefront
- **AI-Powered Features** — demand forecasting, smart search, recommendations

For the full project overview, see the [main project README](../README.md).

---

## Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14+ | React framework (App Router) |
| React | 18+ | UI library |
| TypeScript | 5+ | Type safety |
| Tailwind CSS | 3+ | Utility-first styling |
| Shadcn/UI | latest | Component library |
| Zustand | 4+ | State management |
| React Query | 5+ | Server-state / data fetching |
| Zod | latest | Schema validation |
| Vitest | latest | Unit & integration testing |

---

## Directory Structure

```
frontend/
├── app/            # Next.js App Router — pages, layouts, route handlers
├── components/     # Reusable UI components (atoms, molecules, organisms)
├── constants/      # Application-wide constants and enums
├── hooks/          # Custom React hooks
├── lib/            # Utility functions, API clients, helpers
├── public/         # Static assets (images, fonts, icons)
├── services/       # API service layer (backend communication)
├── stores/         # Zustand state stores
├── styles/         # Global styles, Tailwind config, theme
├── types/          # TypeScript type definitions and interfaces
├── __tests__/      # Test files (unit, integration, e2e)
├── .env.example    # Environment variable template
├── package.json    # Dependencies and scripts
└── README.md       # This file
```

---

## Prerequisites

- **Node.js** ≥ 18 LTS
- **pnpm** ≥ 8 (recommended) or npm ≥ 9
- **Git** ≥ 2.40

---

## Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
pnpm install        # or: npm install

# 3. Copy environment template and configure
cp .env.example .env.local

# 4. Start the development server
pnpm dev            # or: npm run dev
```

The application will be available at **http://localhost:3000**.

---

## Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server |
| `pnpm build` | Create production build |
| `pnpm start` | Start production server |
| `pnpm lint` | Run ESLint |
| `pnpm test` | Run tests (Vitest) |
| `pnpm type-check` | TypeScript type checking (`tsc --noEmit`) |

---

## Architecture

### App Router

The frontend uses the **Next.js App Router** (`app/` directory) which provides:

- File-system based routing
- Nested layouts
- Server Components by default
- Streaming and Suspense
- Route handlers for API endpoints

### Component Organization

Components follow the **atomic design** pattern:

- **Atoms** — basic UI elements (buttons, inputs, badges)
- **Molecules** — small composites (search bar, card)
- **Organisms** — complex sections (navigation, data tables)

### State Management

- **Server state** is managed via **React Query** (caching, re-fetching, optimistic updates).
- **Client state** is managed via **Zustand** stores (UI state, user preferences, cart).

---

## Testing

### Running Tests

```bash
pnpm test              # Run all tests
pnpm test --watch      # Watch mode
pnpm test --coverage   # With coverage report
```

### Writing Tests

- Place test files in `__tests__/` or co-locate with `*.test.ts(x)` suffix.
- Use **Vitest** + **React Testing Library** for component tests.
- Aim for **≥ 80 %** code coverage on critical paths.

---

## Components

The project uses **Shadcn/UI** as the base component library, built on top of **Radix UI** primitives and styled with **Tailwind CSS**. Components are installed individually and can be fully customised.

---

## Further Reading

- [Main Project README](../README.md)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Shadcn/UI Documentation](https://ui.shadcn.com)
