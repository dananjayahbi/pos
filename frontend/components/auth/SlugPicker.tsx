'use client';

import { useState, useEffect } from 'react';
import { useDebounce } from '@/hooks/useDebounce';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { CheckCircle, XCircle, Loader2 } from 'lucide-react';

interface SlugPickerProps {
  value: string;
  onChange: (slug: string) => void;
  onAvailabilityChange?: (available: boolean) => void;
  disabled?: boolean;
}

const BASE_DOMAIN = process.env.NEXT_PUBLIC_ROOT_DOMAIN ?? 'localhost';

export function SlugPicker({ value, onChange, onAvailabilityChange, disabled }: SlugPickerProps) {
  const [status, setStatus] = useState<'idle' | 'checking' | 'available' | 'taken' | 'invalid'>(
    'idle'
  );
  const debouncedSlug = useDebounce(value, 400);

  useEffect(() => {
    if (!debouncedSlug || debouncedSlug.length < 3) {
      setStatus('idle');
      return;
    }

    if (!/^[a-z0-9][a-z0-9\-]{1,30}[a-z0-9]$/.test(debouncedSlug)) {
      setStatus('invalid');
      onAvailabilityChange?.(false);
      return;
    }

    setStatus('checking');
    const apiBase = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';
    fetch(`${apiBase}/tenants/check-slug/?slug=${encodeURIComponent(debouncedSlug)}`)
      .then((r) => r.json())
      .then((data) => {
        const available = data.available === true;
        setStatus(available ? 'available' : 'taken');
        onAvailabilityChange?.(available);
      })
      .catch(() => {
        setStatus('idle');
        onAvailabilityChange?.(false);
      });
  }, [debouncedSlug, onAvailabilityChange]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const normalized = e.target.value
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9\-]/g, '');
    onChange(normalized);
  };

  return (
    <div className="space-y-2">
      <Label htmlFor="slug">Your Store URL</Label>

      <div className="flex items-center gap-0">
        <div className="flex items-center rounded-l-md border border-r-0 bg-muted px-3 h-10 text-sm text-muted-foreground">
          https://
        </div>
        <Input
          id="slug"
          value={value}
          onChange={handleChange}
          placeholder="your-store"
          className="rounded-none"
          maxLength={32}
          disabled={disabled}
        />
        <div className="flex items-center rounded-r-md border border-l-0 bg-muted px-3 h-10 text-sm text-muted-foreground">
          .{BASE_DOMAIN}
        </div>
      </div>

      <div className="flex items-center gap-1.5 text-sm h-5">
        {status === 'checking' && (
          <>
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            <span className="text-muted-foreground">Checking availability...</span>
          </>
        )}
        {status === 'available' && (
          <>
            <CheckCircle className="h-4 w-4 text-green-500" />
            <span className="text-green-600">
              {value}.{BASE_DOMAIN} is available!
            </span>
          </>
        )}
        {status === 'taken' && (
          <>
            <XCircle className="h-4 w-4 text-destructive" />
            <span className="text-destructive">
              {value}.{BASE_DOMAIN} is already taken.
            </span>
          </>
        )}
        {status === 'invalid' && (
          <>
            <XCircle className="h-4 w-4 text-destructive" />
            <span className="text-destructive">
              Use 3-32 lowercase letters, digits, or hyphens.
            </span>
          </>
        )}
      </div>

      <p className="text-xs text-muted-foreground">
        This will be your permanent store address. Choose carefully — it cannot be changed later.
      </p>
    </div>
  );
}
