'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchTenantDomains,
  addTenantDomain,
  deleteTenantDomain,
  verifyTenantDomain,
} from '@/lib/api/tenant';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Globe, Trash2, CheckCircle2, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';

export default function DomainsSettingsPage() {
  const queryClient = useQueryClient();
  const [newDomain, setNewDomain] = useState('');
  const [pendingVerification, setPendingVerification] = useState<{
    id: number;
    domain: string;
    instructions: {
      type: string;
      name: string;
      value: string;
      description: string;
    };
  } | null>(null);

  const { data: domains = [], isLoading } = useQuery({
    queryKey: ['tenant-domains'],
    queryFn: fetchTenantDomains,
  });

  const addMutation = useMutation({
    mutationFn: (domain: string) => addTenantDomain(domain),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['tenant-domains'] });
      setNewDomain('');
      if (result.verification_instructions) {
        setPendingVerification({
          id: result.id,
          domain: result.domain,
          instructions: result.verification_instructions,
        });
      }
      toast.success('Domain added. Please verify ownership.');
    },
    onError: (err: unknown) => {
      const msg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error;
      toast.error(msg ?? 'Failed to add domain.');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTenantDomain,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tenant-domains'] });
      toast.success('Domain removed.');
    },
    onError: () => toast.error('Failed to remove domain.'),
  });

  const verifyMutation = useMutation({
    mutationFn: verifyTenantDomain,
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['tenant-domains'] });
      if (result.verified) {
        toast.success('Domain verified successfully!');
        setPendingVerification(null);
      } else {
        toast.error(result.message);
      }
    },
    onError: () => toast.error('Verification check failed.'),
  });

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-xl font-semibold">Custom Domains</h2>
        <p className="text-sm text-muted-foreground">
          Add your own domain name to access the system.
        </p>
      </div>

      {/* Add Domain */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Add Custom Domain</CardTitle>
          <CardDescription>
            Enter a domain you own (e.g., <code>shop.yourbusiness.com</code>). You will need to add
            a DNS record to verify ownership.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (newDomain.trim()) addMutation.mutate(newDomain.trim());
            }}
            className="flex gap-2"
          >
            <Input
              placeholder="shop.yourbusiness.com"
              value={newDomain}
              onChange={(e) => setNewDomain(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={!newDomain.trim() || addMutation.isPending}>
              Add Domain
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Pending Verification Instructions */}
      {pendingVerification && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Verify {pendingVerification.domain}</AlertTitle>
          <AlertDescription className="space-y-3">
            <p>{pendingVerification.instructions.description}</p>
            <div className="bg-muted rounded p-3 font-mono text-xs space-y-1">
              <div>
                <span className="text-muted-foreground">Type: </span>
                {pendingVerification.instructions.type}
              </div>
              <div>
                <span className="text-muted-foreground">Name: </span>
                {pendingVerification.instructions.name}.{pendingVerification.domain}
              </div>
              <div>
                <span className="text-muted-foreground">Value: </span>
                {pendingVerification.instructions.value}
              </div>
            </div>
            <Button
              size="sm"
              onClick={() => verifyMutation.mutate(pendingVerification.id)}
              disabled={verifyMutation.isPending}
            >
              Check Verification
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Domain List */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Your Domains</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-2">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 bg-muted rounded animate-pulse" />
              ))}
            </div>
          ) : domains.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-6">
              No custom domains added yet.
            </p>
          ) : (
            <div className="space-y-2">
              {domains.map((domain) => (
                <div
                  key={domain.id}
                  className="flex items-center gap-3 py-2 border-b last:border-0"
                >
                  <Globe className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <span className="flex-1 font-mono text-sm">{domain.domain}</span>
                  {domain.is_primary && (
                    <Badge variant="outline" className="text-xs">
                      Primary
                    </Badge>
                  )}
                  {domain.is_verified ? (
                    <span className="flex items-center gap-1 text-xs text-green-600">
                      <CheckCircle2 className="h-3 w-3" /> Verified
                    </span>
                  ) : (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-xs h-7"
                      onClick={() => verifyMutation.mutate(domain.id)}
                      disabled={verifyMutation.isPending}
                    >
                      Check Verification
                    </Button>
                  )}
                  {!domain.is_primary && (
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 text-muted-foreground hover:text-destructive"
                      onClick={() => {
                        if (confirm(`Remove ${domain.domain}?`)) {
                          deleteMutation.mutate(domain.id);
                        }
                      }}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
