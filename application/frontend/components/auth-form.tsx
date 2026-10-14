'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'

type AuthFormProps = { mode: 'login' | 'register' }

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter()
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const isRegistration = mode === 'register'

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setPending(true)
    const formData = new FormData(event.currentTarget)
    const body = Object.fromEntries(formData.entries())

    try {
      const response = await fetch(`/api/auth/${mode}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!response.ok) {
        const result = (await response.json()) as { error?: string }
        setError(result.error ?? 'Unable to continue. Please try again.')
        return
      }
      router.replace('/workspace')
      router.refresh()
    } catch {
      setError('Unable to reach the service. Please try again.')
    } finally {
      setPending(false)
    }
  }

  return (
    <form className="mt-8 space-y-5" onSubmit={submit}>
      {isRegistration && (
        <div>
          <label className="mb-2 block text-sm font-bold text-emerald-950" htmlFor="display_name">Name</label>
          <input className="auth-input" id="display_name" name="display_name" autoComplete="name" minLength={1} maxLength={80} required />
        </div>
      )}
      <div>
        <label className="mb-2 block text-sm font-bold text-emerald-950" htmlFor="email">Email</label>
        <input className="auth-input" id="email" name="email" type="email" autoComplete="email" required />
      </div>
      <div>
        <label className="mb-2 block text-sm font-bold text-emerald-950" htmlFor="password">Password</label>
        <input className="auth-input" id="password" name="password" type="password" autoComplete={isRegistration ? 'new-password' : 'current-password'} minLength={isRegistration ? 12 : 1} maxLength={128} required />
        {isRegistration && <p className="mt-2 text-sm text-slate-500">Use at least 12 characters. Never reuse a healthcare or email password.</p>}
      </div>
      {error ? <p className="rounded-xl border border-red-900/20 bg-red-50 p-3 text-sm text-red-800" role="alert" aria-live="polite">{error}</p> : null}
      <button className="w-full rounded-full bg-teal-700 px-5 py-3.5 font-bold text-white shadow-lg shadow-teal-900/15 outline-none hover:bg-teal-800 focus-visible:ring-3 focus-visible:ring-amber-400 disabled:cursor-wait disabled:opacity-60" disabled={pending} type="submit">
        {pending ? 'Please wait…' : isRegistration ? 'Create account' : 'Sign in'}
      </button>
    </form>
  )
}
