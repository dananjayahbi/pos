import type { LucideIcon } from 'lucide-react';
import {
  LayoutDashboard,
  Package,
  FolderTree,
  Archive,
  RefreshCw,
  Truck,
  ShoppingCart,
  FileText,
  FileCheck,
  Users,
  CreditCard,
  ShoppingBag,
  Receipt,
  Building2,
  UserCircle,
  Clock,
  Wallet,
  Calendar,
  Settings,
  UserCog,
  Shield,
  Key,
  Sliders,
  ArrowLeftRight,
  Warehouse,
  ScrollText,
  Plug,
  BookOpen,
  User,
} from 'lucide-react';

// ── Types ──────────────────────────────────────────────────────

export interface MenuItem {
  id: string;
  label: string;
  icon: LucideIcon;
  path?: string;
  children?: MenuItem[];
  permission?: string | string[];
  badge?: number | string;
  divider?: boolean;
}

// ── Menu structure ─────────────────────────────────────────────

export const navigationMenuItems: MenuItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: LayoutDashboard,
    path: '/dashboard',
  },
  {
    id: 'inventory',
    label: 'Inventory',
    icon: Package,
    permission: 'inventory.view',
    children: [
      {
        id: 'products',
        label: 'Products',
        icon: Package,
        path: '/dashboard/products',
        permission: 'inventory.view_product',
      },
      {
        id: 'categories',
        label: 'Categories',
        icon: FolderTree,
        path: '/dashboard/products/categories',
        permission: 'inventory.view_category',
      },
      {
        id: 'adjustments',
        label: 'Adjustments',
        icon: RefreshCw,
        path: '/inventory/adjustments',
        permission: 'inventory.view_adjustment',
      },
      {
        id: 'movements',
        label: 'Movements',
        icon: ArrowLeftRight,
        path: '/inventory/movements',
        permission: 'inventory.view_movement',
      },
      {
        id: 'transfers',
        label: 'Transfers',
        icon: Truck,
        path: '/inventory/transfers',
        permission: 'inventory.view_transfer',
      },
      {
        id: 'warehouses',
        label: 'Warehouses',
        icon: Warehouse,
        path: '/inventory/warehouses',
        permission: 'inventory.view_warehouse',
      },
    ],
  },
  {
    id: 'sales',
    label: 'Sales',
    icon: ShoppingCart,
    permission: 'sales.view',
    children: [
      {
        id: 'orders',
        label: 'Orders',
        icon: ShoppingCart,
        path: '/orders',
        permission: 'sales.view_order',
      },
      {
        id: 'invoices',
        label: 'Invoices',
        icon: FileText,
        path: '/invoices',
        permission: 'sales.view_invoice',
      },
      {
        id: 'quotes',
        label: 'Quotes',
        icon: FileCheck,
        path: '/quotes',
        permission: 'sales.view_quote',
      },
      {
        id: 'customers',
        label: 'Customers',
        icon: Users,
        path: '/customers',
        permission: 'sales.view_customer',
      },
      {
        id: 'pos',
        label: 'POS',
        icon: CreditCard,
        path: '/pos',
        permission: 'sales.view_pos',
      },
    ],
  },
  {
    id: 'purchasing',
    label: 'Purchasing',
    icon: ShoppingBag,
    permission: 'purchasing.view',
    children: [
      {
        id: 'purchase-orders',
        label: 'Purchase Orders',
        icon: ShoppingBag,
        path: '/purchase-orders',
        permission: 'purchasing.view_order',
      },
      {
        id: 'vendors',
        label: 'Vendors',
        icon: Building2,
        path: '/vendors',
        permission: 'purchasing.view_vendor',
      },
    ],
  },
  {
    id: 'hr',
    label: 'HR',
    icon: UserCircle,
    permission: 'hr.view',
    children: [
      {
        id: 'employees',
        label: 'Employees',
        icon: Users,
        path: '/employees',
        permission: 'hr.view_employee',
      },
      {
        id: 'attendance',
        label: 'Attendance',
        icon: Clock,
        path: '/attendance',
        permission: 'hr.view_attendance',
      },
      {
        id: 'payroll',
        label: 'Payroll',
        icon: Wallet,
        path: '/payroll',
        permission: 'hr.view_payroll',
      },
      {
        id: 'leave',
        label: 'Leave',
        icon: Calendar,
        path: '/leave',
        permission: 'hr.view_leave',
      },
    ],
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: Settings,
    permission: 'settings.view',
    divider: true,
    children: [
      {
        id: 'settings-users',
        label: 'Users',
        icon: UserCog,
        path: '/settings/users',
        permission: 'settings.manage_users',
      },
      {
        id: 'settings-roles',
        label: 'Roles',
        icon: Shield,
        path: '/settings/roles',
        permission: 'settings.manage_roles',
      },
      {
        id: 'settings-company',
        label: 'Company',
        icon: Building2,
        path: '/settings/company',
        permission: 'settings.manage_company',
      },
      {
        id: 'settings-billing',
        label: 'Billing',
        icon: Receipt,
        path: '/settings/billing',
        permission: 'settings.manage_billing',
      },
      {
        id: 'settings-api-keys',
        label: 'API Keys',
        icon: Key,
        path: '/settings/api-keys',
        permission: 'settings.manage_api_keys',
      },
      {
        id: 'settings-audit-log',
        label: 'Audit Log',
        icon: ScrollText,
        path: '/settings/audit-log',
        permission: 'settings.view_audit_log',
      },
      {
        id: 'settings-integrations',
        label: 'Integrations',
        icon: Plug,
        path: '/settings/integrations',
        permission: 'settings.manage_integrations',
      },
      {
        id: 'settings-preferences',
        label: 'Preferences',
        icon: Sliders,
        path: '/settings',
      },
      {
        id: 'settings-profile',
        label: 'My Profile',
        icon: User,
        path: '/settings/profile',
      },
    ],
  },
  {
    id: 'documentation',
    label: 'Documentation',
    icon: BookOpen,
    path: '/documentation',
    divider: true,
  },
];
