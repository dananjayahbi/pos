'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { getPlatformUser, platformLogout } from '@/lib/api/platform';
import { LayoutDashboard, Building2, Users, CreditCard, LogOut, Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

const NAV_ITEMS = [
  { href: '/platform/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/platform/tenants', label: 'Tenants', icon: Building2 },
  { href: '/platform/staff', label: 'Staff', icon: Users },
  { href: '/platform/billing', label: 'Billing', icon: CreditCard },
];

export default function PlatformLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<ReturnType<typeof getPlatformUser>>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [queryClient] = useState(() => new QueryClient());

  useEffect(() => {
    // Skip auth check on login page
    if (pathname === '/platform/login') return;

    const currentUser = getPlatformUser();
    if (!currentUser) {
      router.push('/platform/login');
      return;
    }
    setUser(currentUser);
  }, [pathname, router]);

  // Render login page without layout
  if (pathname === '/platform/login') {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
  }

  // Show nothing while auth check runs
  if (!user) return null;

  const handleLogout = () => {
    platformLogout();
    router.push('/platform/login');
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex h-screen bg-slate-950 text-white overflow-hidden">
        {/* Sidebar */}
        <aside
          className={cn(
            'fixed inset-y-0 left-0 z-50 w-60 bg-slate-900 border-r border-slate-800 flex flex-col transition-transform duration-200',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full',
            'lg:relative lg:translate-x-0'
          )}
        >
          {/* Logo */}
          <div className="flex items-center gap-2 px-4 h-16 border-b border-slate-800">
            <span className="font-bold text-lg">LankaCommerce</span>
            <span className="text-xs bg-blue-600 text-white px-1.5 py-0.5 rounded">PLATFORM</span>
          </div>

          {/* Nav */}
          <nav className="flex-1 py-4 px-2 space-y-1">
            {NAV_ITEMS.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                  pathname === href || pathname.startsWith(href + '/')
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
          </nav>

          {/* User + Logout */}
          <div className="border-t border-slate-800 p-4">
            <div className="text-xs text-slate-400 mb-1">{user.full_name}</div>
            <div className="text-xs text-slate-500 mb-3">{user.role.replace('_', ' ')}</div>
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start text-slate-400 hover:text-white"
              onClick={handleLogout}
            >
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </aside>

        {/* Main */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Top bar (mobile) */}
          <header className="h-16 flex items-center gap-4 px-4 border-b border-slate-800 lg:hidden">
            <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(!sidebarOpen)}>
              {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
            <span className="font-semibold">Platform Admin</span>
          </header>

          <main className="flex-1 overflow-y-auto p-6">{children}</main>
        </div>

        {/* Mobile overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </QueryClientProvider>
  );
}
