import { redirect } from 'next/navigation';

export default function TenantHomePage({ params }: { params: { slug: string } }) {
  // For now, redirect to the ERP dashboard
  // In the future, this could be the webstore or a landing page
  redirect(`/dashboard`);
}
