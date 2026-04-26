'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { useSearchParams, useRouter } from 'next/navigation';
import {
  fetchTenants,
  suspendTenant,
  reactivateTenant,
  type TenantSummary,
} from '@/lib/api/platform';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { MoreHorizontal, Search, ExternalLink } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

function StatusBadge({ status }: { status: TenantSummary['status'] }) {
  const variants: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
    active: 'default',
    suspended: 'destructive',
    archived: 'secondary',
  };
  return (
    <Badge variant={variants[status] ?? 'outline'}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </Badge>
  );
}

export default function PlatformTenantsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['platform-tenants', search, statusFilter, page],
    queryFn: () =>
      fetchTenants({
        search: search || undefined,
        status: statusFilter !== 'all' ? statusFilter : undefined,
        page,
      }),
  });

  const suspendMutation = useMutation({
    mutationFn: suspendTenant,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-tenants'] });
      toast.success('Tenant suspended.');
    },
    onError: () => toast.error('Failed to suspend tenant.'),
  });

  const reactivateMutation = useMutation({
    mutationFn: reactivateTenant,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-tenants'] });
      toast.success('Tenant reactivated.');
    },
    onError: () => toast.error('Failed to reactivate tenant.'),
  });

  const tenants = data?.results ?? [];
  const totalCount = data?.count ?? 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Tenants</h1>
          <p className="text-muted-foreground">{totalCount} total tenants registered</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search by name or email..."
            className="pl-9"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <Select
          value={statusFilter}
          onValueChange={(v) => {
            setStatusFilter(v);
            setPage(1);
          }}
        >
          <SelectTrigger className="w-36">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All statuses</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="suspended">Suspended</SelectItem>
            <SelectItem value="archived">Archived</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Business</TableHead>
              <TableHead>Subdomain</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Trial</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead>Registered</TableHead>
              <TableHead className="w-10" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 7 }).map((_, j) => (
                    <TableCell key={j}>
                      <div className="h-4 bg-muted rounded animate-pulse" />
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : tenants.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center py-8 text-muted-foreground">
                  No tenants found.
                </TableCell>
              </TableRow>
            ) : (
              tenants.map((tenant) => (
                <TableRow key={tenant.schema_name}>
                  <TableCell>
                    <div className="font-medium">{tenant.name}</div>
                    <div className="text-xs text-muted-foreground">{tenant.industry}</div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <span className="text-sm font-mono">{tenant.slug}</span>
                      {tenant.primary_domain && (
                        <a
                          href={`http://${tenant.primary_domain}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-muted-foreground hover:text-foreground"
                        >
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={tenant.status} />
                  </TableCell>
                  <TableCell>
                    {tenant.on_trial ? (
                      <span
                        className={
                          (tenant.days_in_trial ?? 0) <= 2
                            ? 'text-destructive text-sm font-medium'
                            : 'text-sm'
                        }
                      >
                        {tenant.days_in_trial != null && tenant.days_in_trial >= 0
                          ? `${tenant.days_in_trial}d left`
                          : 'Expired'}
                      </span>
                    ) : (
                      <span className="text-sm text-muted-foreground">Paid</span>
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="text-sm">{tenant.contact_email}</div>
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {formatDistanceToNow(new Date(tenant.created), { addSuffix: true })}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem asChild>
                          <Link href={`/platform/tenants/${tenant.schema_name}`}>View Details</Link>
                        </DropdownMenuItem>
                        {tenant.status === 'active' ? (
                          <DropdownMenuItem
                            className="text-destructive"
                            onClick={() => suspendMutation.mutate(tenant.schema_name)}
                          >
                            Suspend
                          </DropdownMenuItem>
                        ) : tenant.status === 'suspended' ? (
                          <DropdownMenuItem
                            onClick={() => reactivateMutation.mutate(tenant.schema_name)}
                          >
                            Reactivate
                          </DropdownMenuItem>
                        ) : null}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {totalCount > 25 && (
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
          >
            Previous
          </Button>
          <span className="text-sm text-muted-foreground">Page {page}</span>
          <Button
            variant="outline"
            size="sm"
            disabled={!data?.next}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}
