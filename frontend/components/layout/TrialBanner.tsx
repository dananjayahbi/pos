'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchTenantInfo } from '@/lib/api/tenant';
import { AlertTriangle, X } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

export function TrialBanner() {
  const [dismissed, setDismissed] = useState(false);

  const { data: tenantInfo } = useQuery({
    queryKey: ['tenant-info'],
    queryFn: fetchTenantInfo,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (!tenantInfo?.on_trial || dismissed) {
    return null;
  }

  const daysLeft = tenantInfo.days_left ?? 0;
  const isExpired = daysLeft < 0;
  const isUrgent = daysLeft <= 3 && !isExpired;

  return (
    <div
      className={cn(
        'w-full px-4 py-2 flex items-center justify-between text-sm',
        isExpired
          ? 'bg-destructive text-destructive-foreground'
          : isUrgent
            ? 'bg-orange-500 text-white'
            : 'bg-yellow-400 text-yellow-900'
      )}
    >
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-4 w-4 flex-shrink-0" />
        {isExpired ? (
          <span>Your free trial has expired. Please upgrade your subscription to continue.</span>
        ) : (
          <span>
            You are on a free trial.{' '}
            <strong>
              {daysLeft} day{daysLeft !== 1 ? 's' : ''} remaining.
            </strong>{' '}
            Upgrade before your trial ends.
          </span>
        )}
      </div>
      {!isExpired && (
        <button
          onClick={() => setDismissed(true)}
          className="ml-4 opacity-70 hover:opacity-100 flex-shrink-0"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
