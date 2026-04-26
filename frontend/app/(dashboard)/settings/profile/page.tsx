import type { Metadata } from 'next';
import { createSettingsMetadata } from '@/lib/metadata/settings';

export const metadata: Metadata = createSettingsMetadata(
  'My Profile',
  'Update your personal information, password, and notification preferences.'
);

export default function ProfileSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">My Profile</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Update your personal information, password, and notification preferences.
        </p>
      </div>

      <div className="grid gap-6">
        {/* Personal Information */}
        <section className="rounded-lg border bg-card p-6 shadow-sm">
          <h2 className="text-lg font-medium mb-4">Personal Information</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-1">
              <label className="text-sm font-medium text-foreground">First Name</label>
              <div className="h-10 rounded-md border bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
                Coming soon
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-foreground">Last Name</label>
              <div className="h-10 rounded-md border bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
                Coming soon
              </div>
            </div>
            <div className="space-y-1 sm:col-span-2">
              <label className="text-sm font-medium text-foreground">Email Address</label>
              <div className="h-10 rounded-md border bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
                Coming soon
              </div>
            </div>
          </div>
        </section>

        {/* Change Password */}
        <section className="rounded-lg border bg-card p-6 shadow-sm">
          <h2 className="text-lg font-medium mb-4">Change Password</h2>
          <div className="grid gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-foreground">Current Password</label>
              <div className="h-10 rounded-md border bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
                ••••••••
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-foreground">New Password</label>
              <div className="h-10 rounded-md border bg-muted/30 px-3 py-2 text-sm text-muted-foreground">
                ••••••••
              </div>
            </div>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            Profile editing will be available in an upcoming update.
          </p>
        </section>
      </div>
    </div>
  );
}
