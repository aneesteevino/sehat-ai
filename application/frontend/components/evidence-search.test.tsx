import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import { EvidenceSearch } from './evidence-search'

const fetchMock = jest.fn()

describe('EvidenceSearch', () => {
  beforeEach(() => {
    Object.defineProperty(global, 'fetch', { configurable: true, value: fetchMock })
  })

  afterEach(() => fetchMock.mockReset())

  it('renders evidence with a traceable source and explicit non-answer boundary', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({
        query: 'How long should hands be scrubbed?',
        generated_answer: null,
        disclaimer: 'Evidence retrieval only; no medical answer has been generated.',
        evidence: [{
          chunk_id: 'chunk-1',
          content: 'Scrub all hand surfaces for about 20 seconds.',
          score: 0.8,
          content_trust: 'untrusted',
          citation: {
            source_id: 'cdc-handwashing-faq',
            source_version_id: 'version-1',
            title: 'Hand Hygiene Frequently Asked Questions',
            publisher: 'CDC',
            canonical_url: 'https://www.cdc.gov/clean-hands/faq/',
            locator: 'paragraph 2',
          },
        }],
      }),
    })
    render(<EvidenceSearch />)

    fireEvent.change(screen.getByLabelText('Evidence question'), { target: { value: 'How long should hands be scrubbed?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search evidence' }))

    await waitFor(() => expect(screen.getByText(/20 seconds/i)).toBeVisible())
    expect(fetchMock).toHaveBeenCalledWith('/api/knowledge/search', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ query: 'How long should hands be scrubbed?', limit: 5 }),
    }))
    expect(screen.getByRole('link', { name: /hand hygiene/i })).toHaveAttribute('href', 'https://www.cdc.gov/clean-hands/faq/')
    expect(screen.getByText(/no medical answer/i)).toBeVisible()
  })

  it('shows a safe availability error', async () => {
    fetchMock.mockResolvedValue({ ok: false, json: async () => ({ error: 'Evidence search is unavailable.' }) })
    render(<EvidenceSearch />)

    fireEvent.change(screen.getByLabelText('Evidence question'), { target: { value: 'influenza symptoms' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search evidence' }))

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/unavailable/i))
  })
})
