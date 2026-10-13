'use client'

import { useEffect, useState } from 'react'

type ApiState = 'checking' | 'ready' | 'unavailable'

const statusCopy: Record<ApiState, readonly [string, string]> = {
  checking: ['Checking API', 'Connecting to the local health service…'],
  ready: ['API ready', 'The local foundation is responding normally.'],
  unavailable: ['API offline', 'Start the local FastAPI service to connect this interface.'],
}

const stateStyles: Record<ApiState, string> = {
  checking: 'bg-amber-700 ring-amber-100',
  ready: 'bg-teal-700 ring-teal-100',
  unavailable: 'bg-rose-700 ring-rose-100',
}

export function ApiStatus() {
  const [state, setState] = useState<ApiState>('checking')

  useEffect(() => {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 3500)
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://127.0.0.1:8000'

    fetch(`${baseUrl}/health/ready`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error('API readiness check failed')
        setState('ready')
      })
      .catch(() => setState('unavailable'))
      .finally(() => window.clearTimeout(timeout))

    return () => {
      controller.abort()
      window.clearTimeout(timeout)
    }
  }, [])

  return (
    <div
      className="flex items-center gap-3 rounded-2xl bg-emerald-950/5 p-3.5"
      role="status"
      aria-live="polite"
    >
      <span
        className={`size-2.5 shrink-0 rounded-full ring-5 ${stateStyles[state]}`}
        aria-hidden="true"
      />
      <div className="grid gap-0.5">
        <strong className="text-sm text-emerald-950">{statusCopy[state][0]}</strong>
        <span className="text-xs text-slate-600">{statusCopy[state][1]}</span>
      </div>
    </div>
  )
}
