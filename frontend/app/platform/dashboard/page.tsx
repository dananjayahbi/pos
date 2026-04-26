'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchPlatformStats } from '@/lib/api/platform';
import {
  Building2,
  CheckCircle,
  PauseCircle,
  Archive,
  Clock,
  AlertTriangle,
  TrendingUp,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

function StatCard({
  title,
  value,
  icon: Icon,
  color = 'text-foreground',
  loading = false,
}: {
  title: string;
  value: number;
  icon: React.ElementType;
  color?: string;
  loading?: boolean;
}) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center gap-4">
          <div className="p-2 bg-muted rounded-lg">
            <Icon className={`h-5 w-5 ${color}`} />
          </div>
          <div>
            {loading ? (
              <Skeleton className="h-7 w-16 mb-1" />
            ) : (
              <div className="text-2xl font-bold">{value.toLocaleString()}</div>
            )}
            <div className="text-sm text-muted-foreground">{title}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default function PlatformDashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['platform-stats'],
    queryFn: fetchPlatformStats,
    refetchInterval: 60_000, // refresh every minute
  });

  const stats = data?.tenants;

  if (error) {
    return (
      <div className="flex items-center gap-2 text-destructive">
        <AlertTriangle className="h-4 w-4" />
        Failed to load dashboard stats. Please try again.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Platform Dashboard</h1>
        <p className="text-muted-foreground">Overview of all tenants and platform activity.</p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <StatCard
          title="Total Tenants"
          value={stats?.total ?? 0}
          icon={Building2}
          loading={isLoading}
        />
        <StatCard
          title="Active"
          value={stats?.active ?? 0}
          icon={CheckCircle}
          color="text-green-500"
          loading={isLoading}
        />
        <StatCard
          title="Suspended"
          value={stats?.suspended ?? 0}
          icon={PauseCircle}
          color="text-yellow-500"
          loading={isLoading}
        />
        <StatCard
          title="Archived"
          value={stats?.archived ?? 0}
          icon={Archive}
          color="text-muted-foreground"
          loading={isLoading}
        />
        <StatCard
          title="On Trial"
          value={stats?.on_trial ?? 0}
          icon={Clock}
          color="text-blue-500"
          loading={isLoading}
        />
        <StatCard
          title="Trials Expiring Soon"
          value={stats?.trial_expiring_soon ?? 0}
          icon={AlertTriangle}
          color="text-orange-500"
          loading={isLoading}
        />
        <StatCard
          title="New (Last 30 Days)"
          value={stats?.recent_registrations_30d ?? 0}
          icon={TrendingUp}
          color="text-indigo-500"
          loading={isLoading}
        />
      </div>

      {/* Alerts */}
      {!isLoading && (stats?.trial_expiring_soon ?? 0) > 0 && (
        <Card className="border-orange-200 bg-orange-50 dark:bg-orange-950/20">
          <CardContent className="pt-4 pb-4">
            <div className="flex items-center gap-2 text-orange-700 dark:text-orange-400">
              <AlertTriangle className="h-4 w-4" />
              <span className="text-sm font-medium">
                {stats?.trial_expiring_soon} tenant(s) have trials expiring in the next 3 days.
              </span>
              <a
                href="/platform/tenants?on_trial=true"
                className="ml-auto text-xs underline hover:no-underline"
              >
                View Tenants
              </a>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
