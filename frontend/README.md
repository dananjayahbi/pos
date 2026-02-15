# LankaCommerce Cloud — Frontend

Frontend application for the **LankaCommerce Cloud** multi-tenant SaaS ERP platform, designed for Sri Lankan SMEs.

## Overview

The LankaCommerce Cloud frontend is a modern, multi-tenant web application built with Next.js (App Router). It provides:

- **ERP Dashboard** — inventory, sales, purchasing, accounting, HR modules
- **POS Interface** — point-of-sale with offline support
- **Webstore / E-Commerce** — customer-facing storefront
- **AI-Powered Features** — demand forecasting, smart search, recommendations

For the full project overview, see the [main project README](../README.md).

---

## Technology Stack

| Category       | Technology               | Version   |
| -------------- | ------------------------ | --------- |
| **Framework**  | Next.js (App Router)     | 16.x      |
| **Language**   | TypeScript               | 5.x       |
| **Styling**    | Tailwind CSS             | 3.x       |
| **State**      | Zustand                  | (planned) |
| **Icons**      | Lucide React             | 0.x       |
| **Theming**    | next-themes              | 0.x       |
| **Components** | Shadcn/UI                | (planned) |
| **Variants**   | class-variance-authority | 0.7.x     |
| **Utilities**  | clsx + tailwind-merge    | latest    |

---

## Prerequisites

- **Node.js** 20.x LTS or later
- **pnpm** 8.x or later
- **Git** ≥ 2.40

---

## Getting Started

### 1. Install Dependencies

```bash
pnpm install
```

### 2. Set Up Environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your values
```

### 3. Start Development Server

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Available Scripts

| Command           | Description                           |
| ----------------- | ------------------------------------- |
| `pnpm dev`        | Start development server              |
| `pnpm build`      | Build for production                  |
| `pnpm start`      | Start production server               |
| `pnpm lint`       | Run ESLint                            |
| `pnpm format`     | Format code with Prettier             |
| `pnpm type-check` | Run TypeScript check (`tsc --noEmit`) |
| `pnpm test`       | Run tests                             |
| `pnpm clean`      | Remove build artifacts                |
| `pnpm analyze`    | Analyze bundle size                   |

---

## Project Structure

```
frontend/
├── app/             # Next.js App Router (pages, layouts, error boundaries)
├── components/      # React components
│   ├── ui/          # UI primitives (Button, Input, Card, etc.)
│   ├── layout/      # Layout components (Header, Sidebar, Footer)
│   ├── forms/       # Form components (FormField, Select, DatePicker)
│   └── common/      # Shared components (Logo, Avatar, Spinner)
├── hooks/           # Custom React hooks
├── lib/             # Utility functions (utils, cn, formatters)
├── services/        # API services (fetch wrapper, domain services)
├── stores/          # Zustand state stores
├── constants/       # App configuration & constants
├── styles/          # Global styles (variables, animations)
├── types/           # TypeScript type definitions
├── public/          # Static assets (images, icons, fonts)
├── __tests__/       # Test files
└── ...config files  # tsconfig, tailwind, postcss, etc.
```

---

## Linting

This project uses [ESLint](https://eslint.org/) for code quality with Next.js, TypeScript, React, and import ordering rules.

### Commands

```bash
# Run lint check
pnpm lint

# Fix auto-fixable issues
pnpm lint:fix

# Strict mode (fails on warnings — use in CI)
pnpm lint:strict
```

### Configuration

ESLint is configured in `.eslintrc.json`:
- **Next.js core-web-vitals** — Performance and best practices
- **TypeScript** — Type-safe code rules (`@typescript-eslint`)
- **React & React Hooks** — Component and hooks best practices
- **Import ordering** — Consistent import organization

### IDE Setup

Install the **ESLint** extension in VS Code for inline feedback.

---

## Formatting

This project uses [Prettier](https://prettier.io/) for code formatting, integrated with ESLint.

### Commands

```bash
# Format all files
pnpm format

# Check formatting (CI)
pnpm format:check
```

### Configuration

Prettier is configured in `.prettierrc`:
- **Semicolons:** required
- **Quotes:** single (JS), double (JSX)
- **Tab width:** 2 spaces
- **Trailing commas:** ES5
- **Print width:** 80 characters

### IDE Setup

Install the **Prettier** extension in VS Code and enable **Format on Save**.

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

- **Atoms** (`ui/`) — basic UI elements (buttons, inputs, badges)
- **Molecules** (`forms/`) — form composites (form fields, selects)
- **Organisms** (`layout/`) — complex sections (header, sidebar, dashboard)
- **Shared** (`common/`) — cross-cutting components (logo, spinner, toast)

### State Management

- **Server state** will be managed via **React Query** (caching, re-fetching, optimistic updates).
- **Client state** is managed via **Zustand** stores (UI state, user preferences, cart).

---

## Path Aliases

Import using `@/` prefix for clean, absolute imports:

```typescript
import { cn } from '@/lib/cn'
import { api } from '@/services/api'
import { APP_CONFIG } from '@/constants/config'
import { Button } from '@/components/ui/Button'
```

---

## Environment Variables

See `.env.local.example` for all available variables with documentation.

### Quick Start

```bash
cp .env.local.example .env.local
# Edit .env.local with your values
```

### NEXT_PUBLIC\_ Exposure Rules

Next.js uses the `NEXT_PUBLIC_` prefix to control which environment variables
are exposed to the browser bundle:

| Pattern           | Available In              | Bundled? | Example                          |
| ----------------- | ------------------------- | -------- | -------------------------------- |
| `NEXT_PUBLIC_*`   | Client + Server           | ✅ Yes   | `NEXT_PUBLIC_API_URL`            |
| Without prefix    | Server only (API routes, SSR, middleware) | ❌ No    | `NEXTAUTH_SECRET`, `API_BASE_URL` |

**⚠️ Security Rules:**

1. **NEVER** put secrets in `NEXT_PUBLIC_` variables — they are embedded in the
   JavaScript bundle and visible to anyone.
2. Server-only variables (`NEXTAUTH_SECRET`, `API_BASE_URL`) are **never**
   accessible in client-side code (`use client` components, event handlers).
3. `NEXT_PUBLIC_` values are **inlined at build time** — changing them requires
   a rebuild (`next build`).

### Environment File Loading Order (Next.js)

Next.js loads env files in this order (last wins):

| File                   | Loaded When           | Committed? | Purpose                    |
| ---------------------- | --------------------- | ---------- | -------------------------- |
| `.env`                 | Always                | ✅ Yes     | Shared defaults            |
| `.env.development`     | `NODE_ENV=development`| ❌ No      | Dev-specific defaults      |
| `.env.production`      | `NODE_ENV=production` | ❌ No      | Prod-specific defaults     |
| `.env.local`           | Always (except test)  | ❌ No      | Local overrides + secrets  |
| `.env.development.local` | Dev + local         | ❌ No      | Dev-local overrides        |
| `.env.production.local`  | Prod + local        | ❌ No      | Prod-local overrides       |

### TypeScript Support

All env variables are typed in `types/env.d.ts`. Access with full IntelliSense:

```typescript
// ✅ Type-safe access
const apiUrl = process.env.NEXT_PUBLIC_API_URL; // string
const secret = process.env.NEXTAUTH_SECRET;     // string | undefined

// ✅ Feature flag check
if (process.env.NEXT_PUBLIC_ENABLE_POS === "true") {
  // POS module enabled
}
```

### Runtime Validation (Zod)

Environment variables are validated at **server startup** using [Zod v4](https://zod.dev/).
If any required variable is missing or has an invalid format, the server will **fail fast**
with a descriptive error message.

**How it works:**

1. `lib/env.ts` defines Zod schemas for all server and client env vars.
2. `instrumentation.ts` imports `lib/env.ts` on startup (Next.js instrumentation hook).
3. If validation fails, the server prints a formatted error list and exits.

**Example error output:**

```
❌ Invalid environment variables:

  ✗ NEXT_PUBLIC_API_URL: Required
  ✗ NEXTAUTH_SECRET: Required
  ✗ API_TIMEOUT: Expected number, received "abc"
```

**Using the validated env object:**

```typescript
import { env } from "@/lib/env";

// ✅ Validated and typed — guaranteed to exist
const apiUrl = env.NEXT_PUBLIC_API_URL;
const timeout = env.API_TIMEOUT; // number
const posEnabled = env.NEXT_PUBLIC_ENABLE_POS; // boolean
```

**Troubleshooting:**

- Compare your `.env.local` against `.env.local.example` for missing variables.
- Boolean variables accept: `true`, `false`, `1`, `0`, `yes`, `no` (case-insensitive).
- Numeric variables must contain valid numbers (e.g., `30000`, not `30s`).
- URL variables must include the protocol (e.g., `http://localhost:3000`).

### Client vs Server Variables

Environment variables fall into two categories based on the `NEXT_PUBLIC_` prefix:

**Client-exposed variables** (`NEXT_PUBLIC_*`) — bundled into JavaScript, visible
to the browser. Use for non-sensitive configuration:

| Variable | Purpose | Runtime |
| -------- | ------- | ------- |
| `NEXT_PUBLIC_API_URL` | API endpoint for fetch calls | Client + Server |
| `NEXT_PUBLIC_WS_URL` | WebSocket for real-time features | Client + Server |
| `NEXT_PUBLIC_SITE_NAME` | Brand name in UI | Client + Server |
| `NEXT_PUBLIC_APP_NAME` | Short name (PWA, tabs) | Client + Server |
| `NEXT_PUBLIC_ENABLE_POS` | Feature flag for POS module | Client + Server |
| `NEXT_PUBLIC_DEFAULT_CURRENCY` | Display currency (LKR) | Client + Server |
| `NEXT_PUBLIC_GA_TRACKING_ID` | Analytics tracking | Client + Server |

**Server-only variables** (no prefix) — available in API routes, middleware,
`getServerSideProps`, and Server Components. Use for secrets and internal config:

| Variable | Purpose | Runtime |
| -------- | ------- | ------- |
| `NEXTAUTH_SECRET` | JWT signing secret | Server only |
| `NEXTAUTH_URL` | Auth callback URL | Server only |
| `API_BASE_URL` | Internal API base for SSR | Server only |
| `API_TIMEOUT` | Request timeout in ms | Server only |
| `NODE_ENV` | Runtime environment | Server only |
| `STRIPE_SECRET_KEY` | Stripe server-side payments | Server only |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook verification | Server only |
| `SENTRY_AUTH_TOKEN` | Source map uploads (build) | Server only |

**When to use which:**

```typescript
// ✅ Client component — use NEXT_PUBLIC_ variables
"use client";
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ✅ Server component / API route — both are available
import { env } from "@/lib/env";
const secret = env.NEXTAUTH_SECRET;     // server-only
const siteUrl = env.NEXT_PUBLIC_API_URL; // also available server-side

// ❌ WRONG — server-only variable in client code (will be undefined)
"use client";
const secret = process.env.NEXTAUTH_SECRET; // undefined!
```

### Env Helper Usage Conventions

**Always use `lib/env.ts` as the single source of truth** for environment
variables. This ensures runtime validation and type safety.

**Preferred — import from the validated env helper:**

```typescript
import { env } from "@/lib/env";

// ✅ Validated, typed, and guaranteed to exist
const apiUrl = env.NEXT_PUBLIC_API_URL;    // string
const timeout = env.API_TIMEOUT;           // number
const posEnabled = env.NEXT_PUBLIC_ENABLE_POS; // boolean
```

**Avoid — direct `process.env` access in application code:**

```typescript
// ❌ Avoid — no validation, always returns string | undefined
const timeout = process.env.API_TIMEOUT;
const posEnabled = process.env.NEXT_PUBLIC_ENABLE_POS === "true";
```

**When direct access is acceptable:**

- Inside `next.config.js` (runs before the app, cannot import TypeScript)
- Inside configuration files that run at build time
- In client components that only need `NEXT_PUBLIC_*` values where importing
  the env module would cause server-only code to leak into the bundle

**Adding a new variable:**

1. Add to `.env.local.example` with documentation
2. Add to `.env.example` (quick-reference)
3. Add to `types/env.d.ts` for TypeScript support
4. Add the Zod schema to `lib/env.ts` (server or client schema)
5. Add to `.env.local` with the actual value

### All Variables Reference

| Variable | Type | Default | Category |
| -------- | ---- | ------- | -------- |
| `NEXT_PUBLIC_API_URL` | `string` (URL) | `http://localhost:8000/api/v1` | API |
| `NEXT_PUBLIC_WS_URL` | `string` | `ws://localhost:8000/ws` | API |
| `API_BASE_URL` | `string` (URL) | `http://backend:8000/api/v1` | API (server) |
| `API_TIMEOUT` | `number` | `30000` | API (server) |
| `NEXT_PUBLIC_SITE_URL` | `string` (URL) | `http://localhost:3000` | Site |
| `NEXT_PUBLIC_SITE_NAME` | `string` | `LankaCommerce Cloud` | Site |
| `NEXT_PUBLIC_APP_NAME` | `string` | `LCC` | Site |
| `NEXT_PUBLIC_SITE_DESCRIPTION` | `string` | *(SaaS ERP description)* | Site |
| `NEXTAUTH_URL` | `string` (URL) | `http://localhost:3000` | Auth (server) |
| `NEXTAUTH_SECRET` | `string` | *(empty)* | Auth (server) |
| `NEXT_PUBLIC_AUTH_COOKIE_NAME` | `string` | `lcc_auth` | Auth |
| `NEXT_PUBLIC_TOKEN_EXPIRY_BUFFER` | `number` | `60` | Auth |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | `boolean` | `false` | Feature Flags |
| `NEXT_PUBLIC_ENABLE_AI_FEATURES` | `boolean` | `false` | Feature Flags |
| `NEXT_PUBLIC_ENABLE_WEBSTORE` | `boolean` | `true` | Feature Flags |
| `NEXT_PUBLIC_ENABLE_POS` | `boolean` | `true` | Feature Flags |
| `NEXT_PUBLIC_ENABLE_OFFLINE` | `boolean` | `true` | Feature Flags |
| `NEXT_PUBLIC_DEBUG` | `boolean` | `false` | Feature Flags |
| `NEXT_PUBLIC_GA_TRACKING_ID` | `string` | *(empty)* | Analytics |
| `NEXT_PUBLIC_SENTRY_DSN` | `string` | *(empty)* | Monitoring |
| `NEXT_PUBLIC_PAYHERE_MERCHANT_ID` | `string` | *(empty)* | Payments |
| `NEXT_PUBLIC_STRIPE_PUBLIC_KEY` | `string` | *(empty)* | Payments |
| `NEXT_PUBLIC_MAPS_API_KEY` | `string` | *(empty)* | Maps |
| `STRIPE_SECRET_KEY` | `string` | *(empty)* | Payments (server) |
| `STRIPE_WEBHOOK_SECRET` | `string` | *(empty)* | Payments (server) |
| `SENTRY_AUTH_TOKEN` | `string` | *(empty)* | Monitoring (server) |
| `NEXT_PUBLIC_DEFAULT_LOCALE` | `string` | `en-LK` | Localization |
| `NEXT_PUBLIC_DEFAULT_TIMEZONE` | `string` | `Asia/Colombo` | Localization |
| `NEXT_PUBLIC_DEFAULT_CURRENCY` | `string` | `LKR` | Localization |
| `NEXT_PUBLIC_CURRENCY_SYMBOL` | `string` | `Rs.` | Localization |
| `NEXT_PUBLIC_DEFAULT_TENANT` | `string` | `demo` | Tenant |
| `NEXT_PUBLIC_TENANT_PATTERN` | `string` | `{tenant}.lankacommerce.lk` | Tenant |
| `NEXT_PUBLIC_IMAGE_DOMAIN` | `string` | `cdn.lankacommerce.lk` | Image/CDN |
| `NEXT_PUBLIC_CLOUDINARY_CLOUD` | `string` | *(empty)* | Image/CDN |

---

## Sri Lanka Specifics

- **Currency:** LKR (₨) with 2 decimal places
- **Timezone:** Asia/Colombo
- **Phone format:** +94 XX XXX XXXX
- **Date format:** DD/MM/YYYY

---

## Testing

```bash
pnpm test              # Run all tests
pnpm test --watch      # Watch mode
pnpm test --coverage   # With coverage report
```

---

## Further Reading

- [Main Project README](../README.md)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Zustand Documentation](https://zustand.docs.pmnd.rs)
- [Lucide Icons](https://lucide.dev/icons)
- [Shadcn/UI Documentation](https://ui.shadcn.com)
