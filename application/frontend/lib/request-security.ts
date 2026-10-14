const MAX_AUTH_BODY_BYTES = 8 * 1024

export class AuthRequestError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message)
  }
}

export function validateMutationRequest(request: Request) {
  const fetchSite = request.headers.get('sec-fetch-site')
  if (fetchSite && fetchSite !== 'same-origin' && fetchSite !== 'none') {
    throw new AuthRequestError(403, 'Cross-site requests are not allowed.')
  }

  const origin = request.headers.get('origin')
  if (origin && origin !== new URL(request.url).origin) {
    throw new AuthRequestError(403, 'Cross-site requests are not allowed.')
  }
}

export async function readAuthPayload(request: Request): Promise<Record<string, unknown>> {
  validateMutationRequest(request)

  if (request.headers.get('content-type')?.split(';', 1)[0] !== 'application/json') {
    throw new AuthRequestError(415, 'The request must contain JSON.')
  }

  const declaredLength = Number(request.headers.get('content-length') ?? 0)
  if (declaredLength > MAX_AUTH_BODY_BYTES) {
    throw new AuthRequestError(413, 'The request is too large.')
  }

  const body = await request.text()
  if (new TextEncoder().encode(body).byteLength > MAX_AUTH_BODY_BYTES) {
    throw new AuthRequestError(413, 'The request is too large.')
  }

  try {
    const payload: unknown = JSON.parse(body)
    if (!payload || Array.isArray(payload) || typeof payload !== 'object') {
      throw new AuthRequestError(400, 'The request body is invalid.')
    }
    return payload as Record<string, unknown>
  } catch (error) {
    if (error instanceof AuthRequestError) throw error
    throw new AuthRequestError(400, 'The request body is invalid.')
  }
}
