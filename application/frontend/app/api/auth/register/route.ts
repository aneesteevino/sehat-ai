import { NextResponse } from 'next/server'

import { backendUrl, type BackendSession, SESSION_COOKIE, SESSION_COOKIE_OPTIONS } from '@/lib/auth'
import { AuthRequestError, readAuthPayload } from '@/lib/request-security'

export async function POST(request: Request) {
  let payload: Record<string, unknown>
  try {
    payload = await readAuthPayload(request)
  } catch (error) {
    if (error instanceof AuthRequestError) {
      return NextResponse.json({ error: error.message }, { status: error.status })
    }
    return NextResponse.json({ error: 'The request body is invalid.' }, { status: 400 })
  }

  try {
    const registration = await fetch(backendUrl('/api/v1/auth/register'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      cache: 'no-store',
    })
    if (!registration.ok) {
      const status = registration.status === 409 || registration.status === 422 ? registration.status : 502
      const error = registration.status === 409
        ? 'An account with this email already exists.'
        : 'Check the form and try again.'
      return NextResponse.json({ error }, { status })
    }

    const login = await fetch(backendUrl('/api/v1/auth/login'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: payload.email, password: payload.password }),
      cache: 'no-store',
    })
    if (!login.ok) {
      return NextResponse.json({ error: 'Account created. Please sign in.' }, { status: 502 })
    }

    const session = (await login.json()) as BackendSession
    const response = NextResponse.json({ user: session.user }, { status: 201 })
    response.cookies.set(SESSION_COOKIE, session.access_token, {
      ...SESSION_COOKIE_OPTIONS,
      maxAge: session.expires_in,
    })
    response.headers.set('Cache-Control', 'no-store')
    return response
  } catch {
    return NextResponse.json({ error: 'The account service is unavailable.' }, { status: 503 })
  }
}
