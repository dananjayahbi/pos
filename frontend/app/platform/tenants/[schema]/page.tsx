'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchTenantDetail,
  suspendTenant,
  reactivateTenant,
  extendTenantTrial,
} from '@/lib/api/platform';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft, ExternalLink, AlertTriangle, CheckCircle } from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';
import { format } from 'date-fns';

export default function TenantDetailPage({ params }: { params: { schema: string } }) {
  const queryClient = useQueryClient();
  const [extendDays, setExtendDays] = useState(7);
  const [showExtendDialog, setShowExtendDialog] = useState(false);
  const [showSuspendConfirm, setShowSuspendConfirm] = useState(false);

  const { data: tenant, isLoading } = useQuery({
    queryKey: ['platform-tenant', params.schema],
    queryFn: () => fetchTenantDetail(params.schema),
  });

  const suspendMutation = useMutation({
    mutationFn: () => suspendTenant(params.schema),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-tenant', params.schema] });
      queryClient.invalidateQueries({ queryKey: ['platform-tenants'] });
      toast.success('Tenant suspended.');
      setShowSuspendConfirm(false);
    },
    onError: () => toast.error('Failed to suspend tenant.'),
  });

  const reactivateMutation = useMutation({
    mutationFn: () => reactivateTenant(params.schema),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-tenant', params.schema] });
      toast.success('Tenant reactivated.');
    },
    onError: () => toast.error('Failed to reactivate tenant.'),
  });

  const extendTrialMutation = useMutation({
    mutationFn: () => extendTenantTrial(params.schema, extendDays),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['platform-tenant', params.schema] });
      toast.success(result.message);
      setShowExtendDialog(false);
    },
    onError: () => toast.error('Failed to extend trial.'),
  });

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="h-6 w-48 bg-muted rounded animate-pulse" />
        <div className="h-40 bg-muted rounded animate-pulse" />
      </div>
    );
  }

  if (!tenant) {
    return <div className="text-muted-foreground">Tenant not found.</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link href="/platform/tenants" className="text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold">{tenant.name}</h1>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>{tenant.slug}</span>
            {tenant.primary_domain && (
              <a
                href={`http://${tenant.primary_domain}`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 hover:text-foreground"
              >
                {tenant.primary_domain}
                <ExternalLink className="h-3 w-3" />
              </a>
            )}
          </div>
        </div>
        <div className="ml-auto flex gap-2">
          {tenant.status === 'active' ? (
            <Button variant="destructive" size="sm" onClick={() => setShowSuspendConfirm(true)}>
              Suspend
            </Button>
          ) : tenant.status === 'suspended' ? (
            <Button
              variant="outline"
              size="sm"
              onClick={() => reactivateMutation.mutate()}
              disabled={reactivateMutation.isPending}
            >
              Reactivate
            </Button>
          ) : null}
          {tenant.on_trial && (
            <Button variant="outline" size="sm" onClick={() => setShowExtendDialog(true)}>
              Extend Trial
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Business Info */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Business Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <Row label="Status">
              <Badge variant={tenant.status === 'active' ? 'default' : 'destructive'}>
                {tenant.status}
              </Badge>
            </Row>
            <Row label="Type">{tenant.business_type.replace('_', ' ')}</Row>
            <Row label="Industry">{tenant.industry.replace('_', ' ')}</Row>
            {tenant.business_registration_number && (
              <Row label="Reg. Number">{tenant.business_registration_number}</Row>
            )}
            <Row label="Schema">{tenant.schema_name}</Row>
          </CardContent>
        </Card>

        {/* Subscription */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Subscription</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <Row label="Plan">{tenant.on_trial ? 'Free Trial' : 'Paid'}</Row>
            {tenant.paid_until && (
              <Row label="Valid Until">{format(new Date(tenant.paid_until), 'dd MMM yyyy')}</Row>
            )}
            {tenant.on_trial && tenant.days_in_trial != null && (
              <Row label="Days Left">
                <span className={tenant.days_in_trial <= 2 ? 'text-destructive font-medium' : ''}>
                  {tenant.days_in_trial >= 0 ? `${tenant.days_in_trial} days` : 'Expired'}
                </span>
              </Row>
            )}
            <Row label="Onboarding">
              {tenant.onboarding_completed ? (
                <span className="flex items-center gap-1 text-green-600">
                  <CheckCircle className="h-3 w-3" /> Complete
                </span>
              ) : (
                `Step ${tenant.onboarding_step}`
              )}
            </Row>
          </CardContent>
        </Card>

        {/* Contact */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Contact</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <Row label="Name">{tenant.contact_name}</Row>
            <Row label="Email">{tenant.contact_email}</Row>
            {tenant.contact_phone && <Row label="Phone">{tenant.contact_phone}</Row>}
            {tenant.city && <Row label="Location">{`${tenant.city}, ${tenant.province}`}</Row>}
          </CardContent>
        </Card>

        {/* Domains */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Domains</CardTitle>
          </CardHeader>
          <CardContent>
            {tenant.domains.length === 0 ? (
              <p className="text-sm text-muted-foreground">No domains configured.</p>
            ) : (
              <div className="space-y-2">
                {tenant.domains.map((d) => (
                  <div key={d.id} className="flex items-center gap-2 text-sm">
                    <span className="font-mono flex-1">{d.domain}</span>
                    {d.is_primary && (
                      <Badge variant="outline" className="text-xs">
                        Primary
                      </Badge>
                    )}
                    <Badge variant={d.is_verified ? 'default' : 'secondary'} className="text-xs">
                      {d.is_verified ? 'Verified' : 'Unverified'}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Suspend Confirm Dialog */}
      <Dialog open={showSuspendConfirm} onOpenChange={setShowSuspendConfirm}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-destructive" />
              Suspend Tenant?
            </DialogTitle>
          </DialogHeader>
          <p className="text-sm text-muted-foreground">
            This will block <strong>{tenant.name}</strong> from accessing the system. Their data
            will be preserved and they can be reactivated later.
          </p>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowSuspendConfirm(false)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() => suspendMutation.mutate()}
              disabled={suspendMutation.isPending}
            >
              Suspend
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Extend Trial Dialog */}
      <Dialog open={showExtendDialog} onOpenChange={setShowExtendDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Extend Trial Period</DialogTitle>
          </DialogHeader>
          <div className="space-y-2">
            <Label>Additional Days</Label>
            <Input
              type="number"
              min={1}
              max={90}
              value={extendDays}
              onChange={(e) => setExtendDays(Number(e.target.value))}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowExtendDialog(false)}>
              Cancel
            </Button>
            <Button
              onClick={() => extendTrialMutation.mutate()}
              disabled={extendTrialMutation.isPending}
            >
              Extend Trial
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex justify-between">
      <span className="text-muted-foreground">{label}</span>
      <span>{children}</span>
    </div>
  );
}
