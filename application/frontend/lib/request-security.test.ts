/** @jest-environment node */

import { AuthRequestError, readAuthPayload, validateMutationRequest } from './request-security'

describe('auth route request security', () => {
  it('rejects cross-site mutations', () => {
    const request = new Request('https://sehat.example/api/auth/logout', {
      method: 'POST',
      headers: { Origin: 'https://attacker.example', 'Sec-Fetch-Site': 'cross-site' },
    })

    expect(() => validateMutationRequest(request)).toThrow(AuthRequestError)
  })

  it('accepts a small same-origin JSON object', async () => {
    const request = new Request('https://sehat.example/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Origin: 'https://sehat.example' },
      body: JSON.stringify({ email: 'person@example.com', password: 'not-a-real-password' }),
    })

    await expect(readAuthPayload(request)).resolves.toMatchObject({
      email: 'person@example.com',
    })
  })

  it('rejects non-JSON and oversized bodies', async () => {
    const wrongType = new Request('https://sehat.example/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: 'hello',
    })
    const tooLarge = new Request('https://sehat.example/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': '9000' },
      body: '{}',
    })

    await expect(readAuthPayload(wrongType)).rejects.toMatchObject({ status: 415 })
    await expect(readAuthPayload(tooLarge)).rejects.toMatchObject({ status: 413 })
  })
})
