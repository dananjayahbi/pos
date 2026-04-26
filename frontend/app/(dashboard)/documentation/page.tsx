import type { Metadata } from 'next';
import { FileText, BookOpen, Code2, LifeBuoy, ExternalLink } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Documentation - LCC',
  description: 'LankaCommerce Cloud documentation, guides, and API reference.',
};

const docSections = [
  {
    icon: BookOpen,
    title: 'Getting Started',
    description: 'Set up your store, configure tenants, and onboard your team.',
    href: '/docs/getting-started',
    external: false,
  },
  {
    icon: FileText,
    title: 'User Guides',
    description: 'Step-by-step guides for inventory, sales, HR, and payroll modules.',
    href: '/docs/user-guides',
    external: false,
  },
  {
    icon: Code2,
    title: 'API Reference',
    description: 'REST API documentation for integrating with LankaCommerce Cloud.',
    href: '/api/v1/schema/',
    external: true,
  },
  {
    icon: LifeBuoy,
    title: 'Support',
    description: 'Contact our support team or browse frequently asked questions.',
    href: 'mailto:support@lankacommerce.lk',
    external: true,
  },
];

export default function DocumentationPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Documentation</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Guides, references, and resources for LankaCommerce Cloud.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {docSections.map(({ icon: Icon, title, description, href, external }) => (
          <a
            key={title}
            href={href}
            target={external ? '_blank' : undefined}
            rel={external ? 'noopener noreferrer' : undefined}
            className="group flex items-start gap-4 rounded-lg border bg-card p-6 shadow-sm transition-colors hover:border-primary/50 hover:bg-accent/40"
          >
            <span className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary group-hover:bg-primary/20">
              <Icon className="h-5 w-5" />
            </span>
            <div className="min-w-0">
              <div className="flex items-center gap-1.5 font-medium">
                {title}
                {external && <ExternalLink className="h-3.5 w-3.5 text-muted-foreground" />}
              </div>
              <p className="mt-1 text-sm text-muted-foreground">{description}</p>
            </div>
          </a>
        ))}
      </div>

      <div className="rounded-lg border border-dashed bg-muted/30 p-6 text-center text-sm text-muted-foreground">
        Full in-app documentation is coming soon. In the meantime, use the API Reference link above
        for technical details.
      </div>
    </div>
  );
}
