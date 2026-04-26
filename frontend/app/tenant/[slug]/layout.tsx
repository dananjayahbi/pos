export default function TenantLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { slug: string };
}) {
  return (
    <>
      {/* TenantContext provider will be added here in Phase 2 */}
      {children}
    </>
  );
}
