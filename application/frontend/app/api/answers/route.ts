import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

import { backendUrl, SESSION_COOKIE } from '@/lib/auth'
import { AuthRequestError, readAuthPayload } from '@/lib/request-security'

export async function POST(request: Request) {
  const token = (await cookies()).get(SESSION_COOKIE)?.value
  if (!token) {
    return NextResponse.json({ error: 'Authentication is required.' }, { status: 401 })
  }

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
    const backendResponse = await fetch(backendUrl('/api/v1/answers'), {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      cache: 'no-store',
    })
    if (!backendResponse.ok) {
      const status = backendResponse.status === 401 || backendResponse.status === 422
        ? backendResponse.status
        : 502
      return NextResponse.json(
        { error: status === 422 ? 'Check the question and try again.' : 'Grounded answers are unavailable.' },
        { status },
      )
    }

    const response = NextResponse.json(await backendResponse.json())
    response.headers.set('Cache-Control', 'no-store')
    return response
  } catch {
    return NextResponse.json({ error: 'Grounded answers are unavailable.' }, { status: 503 })
  }
}
