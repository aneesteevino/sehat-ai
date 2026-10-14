import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import { ControlledWorkflow } from './controlled-workflow'

const fetchMock = jest.fn()

describe('ControlledWorkflow', () => {
  beforeEach(() => {
    Object.defineProperty(global, 'fetch', { configurable: true, value: fetchMock })
    Object.defineProperty(global, 'crypto', {
      configurable: true,
      value: { randomUUID: () => '00000000-0000-4000-8000-000000000001' },
    })
  })

  afterEach(() => fetchMock.mockReset())

  it('shows application-owned emergency routing and provider bypass', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({
        level: 'emergency',
        categories: ['breathing'],
        message: 'This may describe a medical emergency. Contact your local emergency services now.',
        actions: ['Contact local emergency services now.'],
        provider_bypassed: true,
      }),
    })
    render(<ControlledWorkflow />)

    fireEvent.change(screen.getByLabelText('Check an emergency phrase'), {
      target: { value: "Someone can't breathe" },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Run safety check' }))

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/emergency services now/i))
    expect(screen.getByText('AI provider bypassed')).toBeVisible()
  })

  it('starts and advances the fixed questionnaire', async () => {
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'workflow-1', kind: 'symptom_questionnaire', state: 'started', summary: [] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'workflow-1', kind: 'symptom_questionnaire', state: 'collecting', summary: [] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'workflow-1', kind: 'symptom_questionnaire', state: 'review', summary: ['concern:fever', 'duration:days', 'severity:mild'] }),
      })
    render(<ControlledWorkflow />)

    fireEvent.click(screen.getByRole('button', { name: 'Start questionnaire' }))
    await waitFor(() => expect(screen.getByRole('button', { name: 'Begin fixed questions' })).toBeVisible())
    fireEvent.click(screen.getByRole('button', { name: 'Begin fixed questions' }))
    await waitFor(() => expect(screen.getByRole('button', { name: 'Review selections' })).toBeVisible())
    fireEvent.click(screen.getByRole('button', { name: 'Review selections' }))

    await waitFor(() => expect(screen.getByText('Review only — no diagnosis')).toBeVisible())
    expect(screen.getByText('concern: fever')).toBeVisible()
  })
})
