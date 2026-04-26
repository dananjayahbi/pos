/**
 * Platform Admin API Client
 * Communicates with /api/v1/platform/* endpoints
 * Uses PlatformUser JWT authentication (separate from tenant user auth)
 */

import axios from 'axios';

const PLATFORM_TOKEN_KEY = 'platform_access_token';
const PLATFORM_REFRESH_KEY = 'platform_refresh_token';
const PLATFORM_USER_KEY = 'platform_user';

// Separate axios instance for platform API — no tenant headers
// Strip /api/v1 from NEXT_PUBLIC_API_URL to get the bare origin; all paths
// below are absolute (start with /api/v1/platform/) so they resolve correctly.
const API_ORIGIN = (process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8002/api/v1')
  .replace(/\/api\/v\d+\/?$/, '');

const platformApi = axios.create({
  baseURL: API_ORIGIN,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor — inject platform JWT
platformApi.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem(PLATFORM_TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Response interceptor — handle 401 (token expired)
platformApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Could add refresh token logic here in Phase 4
      // For now, redirect to platform login
      if (typeof window !== 'undefined') {
        localStorage.removeItem(PLATFORM_TOKEN_KEY);
        localStorage.removeItem(PLATFORM_REFRESH_KEY);
        window.location.href = '/platform/login';
      }
    }
    return Promise.reject(error);
  }
);

// ─── Auth ─────────────────────────────────────────────────────────────────────

export interface PlatformLoginResponse {
  access: string;
  refresh: string;
  user: {
    id: string;
    email: string;
    full_name: string;
    role: 'super_admin' | 'platform_admin' | 'support' | 'viewer';
    is_super_admin: boolean;
  };
}

export async function platformLogin(
  email: string,
  password: string
): Promise<PlatformLoginResponse> {
  const { data } = await platformApi.post<PlatformLoginResponse>('/api/v1/platform/auth/login/', {
    email,
    password,
  });
  // Store tokens and user profile
  localStorage.setItem(PLATFORM_TOKEN_KEY, data.access);
  localStorage.setItem(PLATFORM_REFRESH_KEY, data.refresh);
  localStorage.setItem(PLATFORM_USER_KEY, JSON.stringify(data.user));
  return data;
}

export function platformLogout() {
  localStorage.removeItem(PLATFORM_TOKEN_KEY);
  localStorage.removeItem(PLATFORM_REFRESH_KEY);
  localStorage.removeItem(PLATFORM_USER_KEY);
}

export function getPlatformUser(): PlatformLoginResponse['user'] | null {
  if (typeof window === 'undefined') return null;
  const token = localStorage.getItem(PLATFORM_TOKEN_KEY);
  if (!token) return null;
  try {
    // Read user profile stored on login (JWT payload does not contain user object)
    const userJson = localStorage.getItem(PLATFORM_USER_KEY);
    if (userJson) return JSON.parse(userJson) as PlatformLoginResponse['user'];
    return null;
  } catch {
    return null;
  }
}

// ─── Dashboard Stats ──────────────────────────────────────────────────────────

export interface PlatformStats {
  tenants: {
    total: number;
    active: number;
    suspended: number;
    archived: number;
    on_trial: number;
    trial_expiring_soon: number;
    recent_registrations_30d: number;
  };
}

export async function fetchPlatformStats(): Promise<PlatformStats> {
  const { data } = await platformApi.get<PlatformStats>('/api/v1/platform/stats/');
  return data;
}

// ─── Tenants ──────────────────────────────────────────────────────────────────

export interface TenantSummary {
  id: string;
  name: string;
  slug: string;
  schema_name: string;
  business_type: string;
  industry: string;
  status: 'active' | 'suspended' | 'archived';
  on_trial: boolean;
  paid_until: string | null;
  days_in_trial: number | null;
  contact_email: string;
  contact_phone: string;
  city: string;
  created: string;
  primary_domain: string | null;
}

export interface TenantDetail extends TenantSummary {
  contact_name: string;
  business_registration_number: string;
  address_line_1: string;
  address_line_2: string;
  district: string;
  province: string;
  postal_code: string;
  language: string;
  timezone: string;
  onboarding_step: number;
  onboarding_completed: boolean;
  domains: {
    id: string;
    domain: string;
    is_primary: boolean;
    domain_type: string;
    is_verified: boolean;
    ssl_status: string;
  }[];
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export async function fetchTenants(params?: {
  status?: string;
  on_trial?: boolean;
  search?: string;
  page?: number;
}): Promise<PaginatedResponse<TenantSummary>> {
  const { data } = await platformApi.get<PaginatedResponse<TenantSummary>>(
    '/api/v1/platform/tenants/',
    { params }
  );
  return data;
}

export async function fetchTenantDetail(schemaName: string): Promise<TenantDetail> {
  const { data } = await platformApi.get<TenantDetail>(`/api/v1/platform/tenants/${schemaName}/`);
  return data;
}

export async function suspendTenant(schemaName: string): Promise<void> {
  await platformApi.post(`/api/v1/platform/tenants/${schemaName}/suspend/`);
}

export async function reactivateTenant(schemaName: string): Promise<void> {
  await platformApi.post(`/api/v1/platform/tenants/${schemaName}/reactivate/`);
}

export async function extendTenantTrial(
  schemaName: string,
  days: number
): Promise<{ message: string; new_paid_until: string }> {
  const { data } = await platformApi.post(`/api/v1/platform/tenants/${schemaName}/extend-trial/`, {
    days,
  });
  return data;
}

// ─── Platform Users (Staff) ───────────────────────────────────────────────────

export interface PlatformStaffMember {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  date_joined: string;
  last_login: string | null;
}

export async function fetchPlatformStaff(): Promise<PlatformStaffMember[]> {
  const { data } = await platformApi.get<PlatformStaffMember[]>('/api/v1/platform/users/');
  return data;
}

export async function createPlatformStaff(payload: {
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  password: string;
  confirm_password: string;
}): Promise<PlatformStaffMember> {
  const { data } = await platformApi.post<PlatformStaffMember>('/api/v1/platform/users/', payload);
  return data;
}

export async function deactivatePlatformStaff(userId: string): Promise<void> {
  await platformApi.delete(`/api/v1/platform/users/${userId}/`);
}

export default platformApi;
