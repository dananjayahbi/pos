'use client';

import { useQuery } from '@tanstack/react-query';
import { fetchTenantInfo } from '@/lib/api/tenant';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, AlertTriangle } from 'lucide-react';
import { format } from 'date-fns';

const PLANS = [
  {
    id: 'basic',
    name: 'Basic',
    price: 'LKR 2,500 / month',
    features: ['Up to 5 users', 'Full POS + Inventory', 'Basic reports', 'Email support'],
    popular: false,
  },
  {
    id: 'professional',
    name: 'Professional',
    price: 'LKR 5,000 / month',
    features: [
      'Up to 20 users',
      'Full POS + Inventory + HR',
      'Advanced reports + exports',
      'Priority support',
      'Custom domain',
    ],
    popular: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 'Contact Us',
    features: [
      'Unlimited users',
      'All modules',
      'Custom integrations',
      'Dedicated support',
      'SLA guarantee',
    ],
    popular: false,
  },
];

export default function SubscriptionPage() {
  const { data: tenantInfo } = useQuery({
    queryKey: ['tenant-info'],
    queryFn: fetchTenantInfo,
    staleTime: 5 * 60 * 1000,
  });

  const isOnTrial = tenantInfo?.on_trial ?? false;
  const daysLeft = tenantInfo?.days_left ?? null;

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold">Subscription</h2>
        <p className="text-sm text-muted-foreground">Manage your subscription plan.</p>
      </div>

      {/* Current Status */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Current Plan</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-lg font-medium">{isOnTrial ? 'Free Trial' : 'Paid Plan'}</span>
              <Badge variant={isOnTrial ? 'secondary' : 'default'}>
                {isOnTrial ? 'Trial' : 'Active'}
              </Badge>
            </div>
            {isOnTrial && daysLeft !== null && (
              <div className="mt-1 flex items-center gap-2 text-sm">
                {daysLeft <= 0 ? (
                  <span className="text-destructive flex items-center gap-1">
                    <AlertTriangle className="h-3 w-3" /> Trial expired
                  </span>
                ) : (
                  <span className={daysLeft <= 3 ? 'text-orange-600' : 'text-muted-foreground'}>
                    {daysLeft} day{daysLeft !== 1 ? 's' : ''} remaining
                    {tenantInfo?.paid_until && (
                      <> (expires {format(new Date(tenantInfo.paid_until), 'dd MMM yyyy')})</>
                    )}
                  </span>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Plan Options */}
      <div>
        <h3 className="text-base font-medium mb-3">Available Plans</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {PLANS.map((plan) => (
            <Card
              key={plan.id}
              className={plan.popular ? 'border-primary ring-1 ring-primary' : ''}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">{plan.name}</CardTitle>
                  {plan.popular && <Badge className="text-xs">Popular</Badge>}
                </div>
                <p className="text-lg font-semibold">{plan.price}</p>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2 text-sm">
                      <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full"
                  variant={plan.popular ? 'default' : 'outline'}
                  onClick={() => {
                    window.open(
                      `mailto:sales@yourcompany.com?subject=Upgrade to ${plan.name}&body=I would like to upgrade my subscription to the ${plan.name} plan.`,
                      '_blank'
                    );
                  }}
                >
                  {plan.id === 'enterprise' ? 'Contact Sales' : 'Get Started'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <p className="text-xs text-muted-foreground">
        To upgrade, contact our team at{' '}
        <a href="mailto:sales@yourcompany.com" className="underline">
          sales@yourcompany.com
        </a>{' '}
        or use the button above. We will activate your plan within 24 hours.
      </p>
    </div>
  );
}
