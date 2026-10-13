import { render, screen } from '@testing-library/react'

import Home from './page'

jest.mock('@/components/api-status', () => ({
  ApiStatus: () => <div>API test state</div>,
}))

describe('Home', () => {
  it('renders the safety boundary and planned capabilities', () => {
    render(<Home />)

    expect(screen.getByRole('heading', { name: /understand health information/i })).toBeVisible()
    expect(screen.getByText(/not medical advice or an emergency service/i)).toBeVisible()
    expect(screen.getByText('Health information assistant')).toBeVisible()
    expect(screen.getByText('API test state')).toBeVisible()
  })
})
