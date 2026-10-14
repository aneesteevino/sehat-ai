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
    const backendResponse = await fetch(backendUrl('/api/v1/auth/login'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      cache: 'no-store',
    })
    if (!backendResponse.ok) {
      return NextResponse.json(
        { error: 'The email or password is incorrect.' },
        { status: backendResponse.status === 401 ? 401 : 502 },
      )
    }

    const session = (await backendResponse.json()) as BackendSession
    const response = NextResponse.json({ user: session.user })
    response.cookies.set(SESSION_COOKIE, session.access_token, {
      ...SESSION_COOKIE_OPTIONS,
      maxAge: session.expires_in,
    })
    response.headers.set('Cache-Control', 'no-store')
    return response
  } catch {
    return NextResponse.json({ error: 'The sign-in service is unavailable.' }, { status: 503 })
  }
}
