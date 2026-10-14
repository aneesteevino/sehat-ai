import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import { GroundedAnswer } from './grounded-answer'

const fetchMock = jest.fn()

describe('GroundedAnswer', () => {
  beforeEach(() => {
    Object.defineProperty(global, 'fetch', { configurable: true, value: fetchMock })
  })

  afterEach(() => fetchMock.mockReset())

  it('visibly separates grounded claims, evidence, uncertainty, and safety limits', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({
        status: 'answered',
        claims: [{ text: 'Scrub all hand surfaces for about 20 seconds.', evidence_ids: ['chunk-1'] }],
        evidence: [{
          chunk_id: 'chunk-1',
          content: 'Scrub all hand surfaces for about 20 seconds.',
          citation: {
            source_version_id: 'version-1',
            title: 'Hand Hygiene Frequently Asked Questions',
            publisher: 'CDC',
            canonical_url: 'https://www.cdc.gov/clean-hands/faq/',
            locator: 'paragraph 2',
          },
        }],
        uncertainty: 'Limited to the approved corpus.',
        safety_notice: 'This is not a diagnosis.',
        abstention_reason: null,
        usage: { provider: 'mock', model: 'deterministic-evidence-v1', estimated_cost_usd: 0, attempts: 1 },
      }),
    })
    render(<GroundedAnswer />)

    fireEvent.change(screen.getByLabelText('Question for grounded answer'), { target: { value: 'How long should hands be scrubbed?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Prepare grounded answer' }))

    await waitFor(() => expect(screen.getByText('Evidence-grounded preview')).toBeVisible())
    expect(screen.getByRole('heading', { name: 'Evidence' })).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Uncertainty' })).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Safety limitations' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'View evidence 1' })).toHaveAttribute('href', '#answer-evidence-chunk-1')
    expect(fetchMock).toHaveBeenCalledWith('/api/answers', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ question: 'How long should hands be scrubbed?' }),
    }))
  })

  it('shows a deterministic abstention without inventing an answer', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({
        status: 'abstained',
        claims: [],
        evidence: [],
        uncertainty: 'The approved evidence is not sufficient to answer this question reliably.',
        safety_notice: 'This is not a diagnosis.',
        abstention_reason: 'insufficient_evidence',
        usage: { provider: 'mock', model: 'deterministic-evidence-v1', estimated_cost_usd: 0, attempts: 0 },
      }),
    })
    render(<GroundedAnswer />)

    fireEvent.change(screen.getByLabelText('Question for grounded answer'), { target: { value: 'What is not in the corpus?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Prepare grounded answer' }))

    await waitFor(() => expect(screen.getByText('Not enough approved evidence')).toBeVisible())
    expect(screen.getByText(/can’t answer this reliably/i)).toBeVisible()
  })
})
