import { redirect } from 'next/navigation';

/**
 * Redirect /sales/invoices/new → /invoices
 * Invoice creation is handled from the invoices list page.
 */
export default function SalesInvoicesNewRedirect() {
  redirect('/invoices');
}
