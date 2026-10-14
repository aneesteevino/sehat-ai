'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function SignOutButton() {
  const router = useRouter()
  const [pending, setPending] = useState(false)

  async function signOut() {
    setPending(true)
    await fetch('/api/auth/logout', { method: 'POST' })
    router.replace('/sign-in')
    router.refresh()
  }

  return <button className="rounded-full border border-emerald-900/15 bg-white px-4 py-2 text-sm font-bold text-emerald-950 outline-none hover:bg-emerald-50 focus-visible:ring-3 focus-visible:ring-amber-400 disabled:cursor-wait disabled:opacity-60" disabled={pending} onClick={signOut} type="button">{pending ? 'Signing out…' : 'Sign out'}</button>
}
