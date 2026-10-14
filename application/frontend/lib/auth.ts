import 'server-only'

import { cookies } from 'next/headers'

export const SESSION_COOKIE = process.env.NODE_ENV === 'production'
  ? '__Host-sehat_session'
  : 'sehat_session'

export const SESSION_COOKIE_OPTIONS = {
  httpOnly: true,
  sameSite: 'strict' as const,
  secure: process.env.NODE_ENV === 'production',
  path: '/',
  priority: 'high' as const,
}

export type AuthenticatedUser = {
  id: string
  email: string
  display_name: string
  role: 'patient' | 'clinician' | 'admin'
}

export type BackendSession = {
  access_token: string
  token_type: 'bearer'
  expires_in: number
  user: AuthenticatedUser
}

export function backendUrl(path: string) {
  const baseUrl = process.env.API_BASE_URL ?? 'http://127.0.0.1:8000'
  return new URL(path, `${baseUrl.replace(/\/$/, '')}/`)
}

export async function currentUser(): Promise<AuthenticatedUser | null> {
  const token = (await cookies()).get(SESSION_COOKIE)?.value
  if (!token) return null

  try {
    const response = await fetch(backendUrl('/api/v1/auth/me'), {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store',
    })
    if (!response.ok) return null
    return (await response.json()) as AuthenticatedUser
  } catch {
    return null
  }
}
