import { redirect } from 'next/navigation';

/**
 * Redirect /inventory/products/new → /dashboard/products/new
 * Products live under the /dashboard/products route group.
 */
export default function InventoryProductsNewRedirect() {
  redirect('/dashboard/products/new');
}
