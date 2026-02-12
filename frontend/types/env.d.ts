/**
 * Environment variable type declarations for LankaCommerce Cloud.
 *
 * Extends NodeJS.ProcessEnv with application-specific environment
 * variables for type-safe access via process.env.
 */

declare namespace NodeJS {
  interface ProcessEnv {
    // ── Next.js ──────────────────────────────────────────────
    readonly NODE_ENV: 'development' | 'production' | 'test';

    // ── Public Variables (available in browser) ──────────────
    /** Backend API base URL. */
    readonly NEXT_PUBLIC_API_URL: string;
    /** Frontend app URL. */
    readonly NEXT_PUBLIC_APP_URL: string;
    /** Current tenant identifier. */
    readonly NEXT_PUBLIC_TENANT_ID?: string;

    // ── Feature Flags ────────────────────────────────────────
    /** Toggle AI features on/off. */
    readonly NEXT_PUBLIC_ENABLE_AI?: string;
    /** Enable demo mode for showcasing. */
    readonly NEXT_PUBLIC_DEMO_MODE?: string;

    // ── Sri Lanka Defaults ───────────────────────────────────
    /** Default currency (LKR). */
    readonly NEXT_PUBLIC_DEFAULT_CURRENCY?: string;
    /** Default timezone (Asia/Colombo). */
    readonly NEXT_PUBLIC_DEFAULT_TIMEZONE?: string;

    // ── Server-Only Variables ────────────────────────────────
    /** Secret for API authentication (server only). */
    readonly API_SECRET?: string;
    /** Database connection string for SSR (server only). */
    readonly DATABASE_URL?: string;
  }
}
