import apiClient from '@/services/api/apiClient';

// ── Tenant Info ──────────────────────────────────────────────────────────────

export interface TenantInfo {
  name: string;
  status: string;
  on_trial: boolean;
  paid_until: string | null;
  days_left: number | null;
}

export async function fetchTenantInfo(): Promise<TenantInfo> {
  const response = await apiClient.get('/tenant/info/');
  return response.data;
}

// ── Tenant Domains ───────────────────────────────────────────────────────────

export interface TenantDomain {
  id: number;
  domain: string;
  is_primary: boolean;
  domain_type: string;
  is_verified: boolean;
  ssl_status: string;
}

export interface DomainAddResponse extends TenantDomain {
  verification_instructions?: {
    type: string;
    name: string;
    value: string;
    description: string;
  };
}

export async function fetchTenantDomains(): Promise<TenantDomain[]> {
  const response = await apiClient.get('/tenant/domains/');
  return response.data;
}

export async function addTenantDomain(domain: string): Promise<DomainAddResponse> {
  const response = await apiClient.post('/tenant/domains/', { domain });
  return response.data;
}

export async function deleteTenantDomain(domainId: number): Promise<void> {
  await apiClient.delete(`/tenant/domains/${domainId}/`);
}

export async function verifyTenantDomain(
  domainId: number
): Promise<{ verified: boolean; message: string }> {
  const response = await apiClient.post(`/tenant/domains/${domainId}/verify/`);
  return response.data;
}
