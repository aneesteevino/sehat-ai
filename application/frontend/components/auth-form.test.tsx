import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import { AuthForm } from './auth-form'

const replace = jest.fn()
const refresh = jest.fn()
const fetchMock = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ replace, refresh }),
}))

describe('AuthForm', () => {
  beforeEach(() => {
    Object.defineProperty(global, 'fetch', { configurable: true, value: fetchMock })
  })

  afterEach(() => {
    fetchMock.mockReset()
    replace.mockClear()
    refresh.mockClear()
  })

  it('renders registration safeguards', () => {
    render(<AuthForm mode="register" />)

    expect(screen.getByLabelText('Name')).toBeRequired()
    expect(screen.getByLabelText('Email')).toHaveAttribute('type', 'email')
    expect(screen.getByLabelText('Password')).toHaveAttribute('minLength', '12')
    expect(screen.getByText(/never reuse/i)).toBeVisible()
  })

  it('shows a safe server error without exposing implementation details', async () => {
    fetchMock.mockResolvedValue({
      ok: false,
      json: async () => ({ error: 'The email or password is incorrect.' }),
    })
    render(<AuthForm mode="login" />)

    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'person@example.com' } })
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'wrong-password' } })
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/incorrect/i))
    expect(global.fetch).toHaveBeenCalledWith('/api/auth/login', expect.objectContaining({ method: 'POST' }))
  })
})
