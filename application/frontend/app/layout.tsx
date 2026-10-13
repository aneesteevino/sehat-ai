import type { Metadata } from 'next'

import './globals.css'

export const metadata: Metadata = {
  title: 'Sehat AI',
  description: 'A safety-first, evidence-grounded healthcare knowledge assistant.',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
