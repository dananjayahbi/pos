import type { Metadata } from 'next';
import type { ReactNode } from 'react';

import { SessionProvider } from '@/components/auth/SessionProvider';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { QueryProvider } from '@/providers/QueryProvider';

export const metadata: Metadata = {
  title: {
    template: '%s | POS-ERP System',
    default: 'Dashboard | POS-ERP System',
  },
  robots: {
    index: false,
    follow: false,
  },
};

/**
 * Dashboard route-group layout.
 *
 * Server component shell that wraps all protected ERP pages with:
 *  1. QueryProvider     — TanStack Query client
 *  2. SessionProvider   — session-expiry monitoring
 *  3. ProtectedRoute    — auth gate + permission checks
 *  4. DashboardLayout   — CSS Grid sidebar/header/content
 */
export default function Layout({ children }: { children: ReactNode }) {
  return (
    <QueryProvider>
      <SessionProvider>
        <ProtectedRoute>
          <DashboardLayout>{children}</DashboardLayout>
        </ProtectedRoute>
      </SessionProvider>
    </QueryProvider>
  );
}
