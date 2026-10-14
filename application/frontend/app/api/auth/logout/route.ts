import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

import { backendUrl, SESSION_COOKIE, SESSION_COOKIE_OPTIONS } from '@/lib/auth'
import { AuthRequestError, validateMutationRequest } from '@/lib/request-security'

export async function POST(request: Request) {
  try {
    validateMutationRequest(request)
  } catch (error) {
    if (error instanceof AuthRequestError) {
      return NextResponse.json({ error: error.message }, { status: error.status })
    }
    return NextResponse.json({ error: 'The request is invalid.' }, { status: 400 })
  }

  const cookieStore = await cookies()
  const token = cookieStore.get(SESSION_COOKIE)?.value

  if (token) {
    try {
      await fetch(backendUrl('/api/v1/auth/logout'), {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        cache: 'no-store',
      })
    } catch {
      // Local cookie removal still completes; the server session expires independently.
    }
  }

  const response = NextResponse.json({ message: 'Signed out.' })
  response.cookies.set(SESSION_COOKIE, '', {
    ...SESSION_COOKIE_OPTIONS,
    maxAge: 0,
  })
  response.headers.set('Cache-Control', 'no-store')
  return response
}
