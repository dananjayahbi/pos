import { CreditCard, AlertCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function PlatformBillingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Billing</h1>
        <p className="text-muted-foreground">Platform-wide subscription billing overview.</p>
      </div>

      <Card>
        <CardContent className="pt-6 flex flex-col items-center gap-4 py-16 text-center">
          <CreditCard className="h-12 w-12 text-muted-foreground" />
          <div>
            <p className="text-lg font-medium">Billing Module Coming Soon</p>
            <p className="text-sm text-muted-foreground max-w-sm mt-1">
              Full billing management including subscription history, invoices, and payment records
              will be available in Phase 4.
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <AlertCircle className="h-4 w-4" />
            For now, manage billing records via Django Admin at{' '}
            <code className="bg-muted px-1 rounded">/admin/</code>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
