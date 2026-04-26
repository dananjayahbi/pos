'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchPlatformStaff,
  createPlatformStaff,
  deactivatePlatformStaff,
  getPlatformUser,
  type PlatformStaffMember,
} from '@/lib/api/platform';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Plus, UserX } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';

const ROLE_LABELS: Record<string, string> = {
  super_admin: 'Super Admin',
  platform_admin: 'Platform Admin',
  support: 'Support',
  viewer: 'Viewer',
};

export default function PlatformStaffPage() {
  const queryClient = useQueryClient();
  const currentUser = getPlatformUser();
  const isSuperAdmin = currentUser?.is_super_admin ?? false;

  const [showAddDialog, setShowAddDialog] = useState(false);
  const [form, setForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    role: 'platform_admin',
    password: '',
    confirm_password: '',
  });

  const { data: staff = [], isLoading } = useQuery({
    queryKey: ['platform-staff'],
    queryFn: fetchPlatformStaff,
  });

  const createMutation = useMutation({
    mutationFn: createPlatformStaff,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-staff'] });
      toast.success('Staff member created.');
      setShowAddDialog(false);
      setForm({
        email: '',
        first_name: '',
        last_name: '',
        role: 'platform_admin',
        password: '',
        confirm_password: '',
      });
    },
    onError: (err: unknown) => {
      const msg = (err as { response?: { data?: { email?: string[]; password?: string[] } } })
        ?.response?.data;
      toast.error(msg?.email?.[0] ?? msg?.password?.[0] ?? 'Failed to create staff member.');
    },
  });

  const deactivateMutation = useMutation({
    mutationFn: deactivatePlatformStaff,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['platform-staff'] });
      toast.success('Staff member deactivated.');
    },
    onError: () => toast.error('Failed to deactivate staff member.'),
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password !== form.confirm_password) {
      toast.error('Passwords do not match.');
      return;
    }
    createMutation.mutate(form);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Platform Staff</h1>
          <p className="text-muted-foreground">Manage platform admin staff members.</p>
        </div>
        {isSuperAdmin && (
          <Button onClick={() => setShowAddDialog(true)}>
            <Plus className="h-4 w-4 mr-2" /> Add Staff
          </Button>
        )}
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Joined</TableHead>
              {isSuperAdmin && <TableHead className="w-10" />}
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 3 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 5 }).map((_, j) => (
                    <TableCell key={j}>
                      <div className="h-4 bg-muted rounded animate-pulse" />
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : staff.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                  No staff members found.
                </TableCell>
              </TableRow>
            ) : (
              staff.map((member) => (
                <TableRow key={member.id}>
                  <TableCell className="font-medium">{member.full_name}</TableCell>
                  <TableCell>{member.email}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{ROLE_LABELS[member.role] ?? member.role}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={member.is_active ? 'default' : 'secondary'}>
                      {member.is_active ? 'Active' : 'Inactive'}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {format(new Date(member.date_joined), 'dd MMM yyyy')}
                  </TableCell>
                  {isSuperAdmin && (
                    <TableCell>
                      {member.id !== currentUser?.id && member.is_active && (
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 text-muted-foreground hover:text-destructive"
                          onClick={() => {
                            if (confirm(`Deactivate ${member.email}?`)) {
                              deactivateMutation.mutate(member.id);
                            }
                          }}
                        >
                          <UserX className="h-4 w-4" />
                        </Button>
                      )}
                    </TableCell>
                  )}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Add Staff Dialog */}
      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Platform Staff</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <Label>First Name</Label>
                <Input
                  value={form.first_name}
                  onChange={(e) => setForm((f) => ({ ...f, first_name: e.target.value }))}
                  required
                />
              </div>
              <div className="space-y-1">
                <Label>Last Name</Label>
                <Input
                  value={form.last_name}
                  onChange={(e) => setForm((f) => ({ ...f, last_name: e.target.value }))}
                  required
                />
              </div>
            </div>
            <div className="space-y-1">
              <Label>Email</Label>
              <Input
                type="email"
                value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                required
              />
            </div>
            <div className="space-y-1">
              <Label>Role</Label>
              <Select value={form.role} onValueChange={(v) => setForm((f) => ({ ...f, role: v }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="platform_admin">Platform Admin</SelectItem>
                  <SelectItem value="support">Support</SelectItem>
                  <SelectItem value="viewer">Viewer</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1">
              <Label>Password</Label>
              <Input
                type="password"
                value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                required
                minLength={8}
              />
            </div>
            <div className="space-y-1">
              <Label>Confirm Password</Label>
              <Input
                type="password"
                value={form.confirm_password}
                onChange={(e) => setForm((f) => ({ ...f, confirm_password: e.target.value }))}
                required
              />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setShowAddDialog(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={createMutation.isPending}>
                Create Staff Member
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
