import apiClient from '@/services/api/apiClient';

export interface RegistrationPayload {
  email: string;
  password: string;
  contact_name: string;
  slug: string;
  business_name: string;
  business_type: string;
  industry: string;
  contact_phone?: string;
  city?: string;
  province?: string;
}

export interface RegistrationResponse {
  tenant_id: string;
  business_name: string;
  slug: string;
  subdomain_url: string;
  trial_ends_at: string;
  admin_email: string;
  message: string;
}

export async function registerTenant(payload: RegistrationPayload): Promise<RegistrationResponse> {
  const { data } = await apiClient.post<RegistrationResponse>('/tenants/register/', payload);
  return data;
}

export async function checkSlugAvailability(
  slug: string
): Promise<{ slug: string; available: boolean; subdomain: string }> {
  const { data } = await apiClient.get('/tenants/check-slug/', { params: { slug } });
  return data;
}
