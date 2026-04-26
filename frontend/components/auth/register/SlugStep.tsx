'use client';

import { useState } from 'react';
import type { UseFormReturn } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form';
import { SlugPicker } from '@/components/auth/SlugPicker';
import type { RegistrationFormData } from '@/lib/validations/register';

interface SlugStepProps {
  form: UseFormReturn<RegistrationFormData>;
  disabled?: boolean;
}

export function SlugStep({ form, disabled }: SlugStepProps) {
  const [slugAvailable, setSlugAvailable] = useState(false);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold">Choose Your Store URL</h3>
        <p className="text-sm text-muted-foreground mt-1">
          Pick a unique subdomain for your business. This is how your customers and team will access
          your store.
        </p>
      </div>

      <FormField
        control={form.control}
        name="slug"
        render={({ field }) => (
          <FormItem>
            <FormControl>
              <SlugPicker
                value={field.value ?? ''}
                onChange={(val) => {
                  field.onChange(val);
                  setSlugAvailable(false);
                }}
                onAvailabilityChange={setSlugAvailable}
                disabled={disabled}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
}
