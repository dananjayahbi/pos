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

See `.env.local.example` for all available variables.

| Pattern         | Meaning                |
| --------------- | ---------------------- |
| `NEXT_PUBLIC_*` | Exposed to the browser |
| Without prefix  | Server-side only       |

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
