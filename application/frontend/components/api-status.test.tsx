import { render, screen, waitFor } from '@testing-library/react'

import { ApiStatus } from './api-status'

describe('ApiStatus', () => {
  afterEach(() => {
    jest.restoreAllMocks()
    delete (globalThis as { fetch?: typeof fetch }).fetch
  })

  it('reports an unavailable local API without hiding the interface', async () => {
    globalThis.fetch = jest.fn().mockRejectedValue(new Error('offline'))
    render(<ApiStatus />)

    await waitFor(() => expect(screen.getByText('API offline')).toBeVisible())
  })

  it('reports a ready API after a successful health check', async () => {
    globalThis.fetch = jest.fn().mockResolvedValue({ ok: true })
    render(<ApiStatus />)

    await waitFor(() => expect(screen.getByText('API ready')).toBeVisible())
    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/health/ready',
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    )
  })
})
