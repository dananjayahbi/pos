import { redirect } from 'next/navigation';

/**
 * Redirect /sales/orders/new → /orders/new
 * Orders live at the top-level /orders route group.
 */
export default function SalesOrdersNewRedirect() {
  redirect('/orders/new');
}
