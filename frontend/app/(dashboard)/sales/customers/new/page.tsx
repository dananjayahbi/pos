import { redirect } from 'next/navigation';

/**
 * Redirect /sales/customers/new → /customers/new
 * Customers live at the top-level /customers route group.
 */
export default function SalesCustomersNewRedirect() {
  redirect('/customers/new');
}
