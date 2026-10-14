import 'server-only'

import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

import { backendUrl, SESSION_COOKIE } from '@/lib/auth'
import { AuthRequestError, readAuthPayload } from '@/lib/request-security'

export async function proxyAuthenticatedJson(
  request: Request,
  backendPath: string,
  unavailableMessage: string,
) {
  const token = (await cookies()).get(SESSION_COOKIE)?.value
  if (!token) return NextResponse.json({ error: 'Authentication is required.' }, { status: 401 })

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
    const backendResponse = await fetch(backendUrl(backendPath), {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      cache: 'no-store',
    })
    if (!backendResponse.ok) {
      const status = [401, 404, 409, 422].includes(backendResponse.status)
        ? backendResponse.status
        : 502
      return NextResponse.json({ error: status === 401 ? 'Authentication is required.' : unavailableMessage }, { status })
    }
    const response = NextResponse.json(await backendResponse.json(), { status: backendResponse.status })
    response.headers.set('Cache-Control', 'no-store')
    return response
  } catch {
    return NextResponse.json({ error: unavailableMessage }, { status: 503 })
  }
}
