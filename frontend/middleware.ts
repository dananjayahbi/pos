import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Next.js Middleware — Subdomain-Aware Routing
 *
 * Routes:
 *   {slug}.localhost:3000/...    → tenant storefront (or tenant dashboard)
 *   localhost:3000/...           → main site (marketing, login, registration)
 *   platform.localhost:3000/...  → platform admin dashboard
 */

const ROOT_DOMAIN = process.env.NEXT_PUBLIC_ROOT_DOMAIN ?? 'localhost';
const PLATFORM_SLUG = 'platform';

// Slugs that are NOT tenants — they are part of the main site
const RESERVED_SLUGS = new Set(['www', 'api', 'admin', 'mail', 'static', 'media', PLATFORM_SLUG]);

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  const host = request.headers.get('host') ?? '';

  // Strip port for comparison
  const hostname = host.split(':')[0];

  // Check if we're on the root domain (e.g., "localhost" or "lankacommerce.lk")
  const isRootDomain = hostname === ROOT_DOMAIN || hostname === `www.${ROOT_DOMAIN}`;

  if (isRootDomain) {
    // Main site: serve as-is (marketing, /login, /register, etc.)
    return NextResponse.next();
  }

  // Extract subdomain slug
  // e.g., "tenant1.localhost" → "tenant1"
  // e.g., "tenant1.lankacommerce.lk" → "tenant1"
  const rootParts = ROOT_DOMAIN.split('.');
  const hostParts = hostname.split('.');

  // Slug is everything before the root domain
  const slug = hostParts.slice(0, hostParts.length - rootParts.length).join('.');

  if (!slug) {
    return NextResponse.next();
  }

  // Platform admin subdomain → serve /platform/* routes
  if (slug === PLATFORM_SLUG) {
    url.pathname = `/platform${url.pathname === '/' ? '/dashboard' : url.pathname}`;
    return NextResponse.rewrite(url);
  }

  // Reserved slugs → redirect to main site
  if (RESERVED_SLUGS.has(slug)) {
    url.hostname = ROOT_DOMAIN;
    url.pathname = '/';
    return NextResponse.redirect(url);
  }

  // Tenant subdomain → rewrite to /tenant/[slug]/* route
  // This allows the app to render tenant-specific pages
  url.pathname = `/tenant/${slug}${url.pathname}`;

  // Forward slug as a header so server components can read it
  const response = NextResponse.rewrite(url);
  response.headers.set('x-tenant-slug', slug);

  return response;
}

export const config = {
  // Run middleware on all paths EXCEPT:
  // - Next.js internals (_next/static, _next/image)
  // - Public files (favicon, images, etc.)
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico|css|js)).*)',
  ],
};
