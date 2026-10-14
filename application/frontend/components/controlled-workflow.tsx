'use client'

import { FormEvent, useState } from 'react'

type SafetyResult = {
  level: 'continue' | 'emergency'
  categories: string[]
  message: string
  actions: string[]
  provider_bypassed: true
}

type Workflow = {
  id: string
  kind: 'symptom_questionnaire'
  state: 'started' | 'collecting' | 'review' | 'completed' | 'cancelled'
  summary: string[]
}

function mutationKey(label: string) {
  return `${label}-${crypto.randomUUID()}`
}

export function ControlledWorkflow() {
  const [safety, setSafety] = useState<SafetyResult | null>(null)
  const [workflow, setWorkflow] = useState<Workflow | null>(null)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  async function post<T extends object>(url: string, payload: object): Promise<T> {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const body = await response.json() as T | { error?: string }
    if (!response.ok) throw new Error('error' in body && body.error ? body.error : 'Request failed.')
    return body as T
  }

  async function checkSafety(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const text = new FormData(event.currentTarget).get('safety_text')?.toString().trim() ?? ''
    if (text.length < 2) return
    setPending(true)
    setError('')
    try {
      setSafety(await post<SafetyResult>('/api/safety/check', { text }))
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Safety check is unavailable.')
    } finally {
      setPending(false)
    }
  }

  async function startWorkflow() {
    setPending(true)
    setError('')
    try {
      setWorkflow(await post<Workflow>('/api/workflows', {
        kind: 'symptom_questionnaire',
        idempotency_key: mutationKey('start'),
      }))
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Workflow service is unavailable.')
    } finally {
      setPending(false)
    }
  }

  async function transition(action: 'begin' | 'submit' | 'complete', payload?: object) {
    if (!workflow) return
    setPending(true)
    setError('')
    try {
      setWorkflow(await post<Workflow>(`/api/workflows/${workflow.id}/transitions`, {
        action,
        idempotency_key: mutationKey(action),
        payload,
      }))
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Workflow transition is unavailable.')
    } finally {
      setPending(false)
    }
  }

  function submitQuestionnaire(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    void transition('submit', {
      concern: form.get('concern'),
      duration: form.get('duration'),
      severity: form.get('severity'),
    })
  }

  return (
    <section className="mt-12 rounded-3xl border border-blue-900/15 bg-blue-50/70 p-6 sm:p-8" aria-labelledby="controlled-workflow-title">
      <p className="text-xs font-extrabold tracking-[.13em] text-blue-700 uppercase">Milestone 6 controlled preview</p>
      <h2 className="mt-3 font-serif text-3xl font-medium tracking-[-.03em] text-slate-950" id="controlled-workflow-title">Safety gate and guided questionnaire</h2>
      <p className="mt-3 max-w-2xl leading-7 text-slate-600">Emergency phrases are checked by application rules before AI. The questionnaire follows fixed steps and does not diagnose or recommend treatment.</p>

      <form className="mt-6" onSubmit={checkSafety}>
        <label className="font-bold text-slate-900" htmlFor="safety-text">Check an emergency phrase</label>
        <div className="mt-2 flex flex-col gap-3 sm:flex-row">
          <input className="auth-input flex-1 bg-white" id="safety-text" name="safety_text" minLength={2} maxLength={500} placeholder="Example: Someone is unresponsive and cannot breathe" required />
          <button className="rounded-full bg-blue-700 px-6 py-3 font-bold text-white disabled:opacity-60" disabled={pending} type="submit">Run safety check</button>
        </div>
      </form>

      {safety ? (
        <div className={`mt-5 rounded-2xl border p-5 ${safety.level === 'emergency' ? 'border-red-300 bg-red-50 text-red-950' : 'border-blue-200 bg-white text-slate-700'}`} role={safety.level === 'emergency' ? 'alert' : 'status'} aria-live="polite">
          <h3 className="font-bold">{safety.level === 'emergency' ? 'Contact emergency services now' : 'No configured red flag detected'}</h3>
          <p className="mt-2 text-sm leading-6">{safety.message}</p>
          {safety.actions.length ? <ul className="mt-3 list-disc pl-5 text-sm">{safety.actions.map((action) => <li key={action}>{action}</li>)}</ul> : null}
          <p className="mt-3 text-xs font-bold uppercase tracking-wide">AI provider bypassed</p>
        </div>
      ) : null}

      <div className="mt-8 border-t border-blue-900/10 pt-7">
        <h3 className="text-xl font-bold text-slate-950">Synthetic symptom questionnaire</h3>
        <p className="mt-2 text-sm leading-6 text-slate-600">Use demonstration selections only. No free-text symptoms are stored in this workflow.</p>
        {!workflow ? <button className="mt-4 rounded-full border border-blue-700 px-5 py-2.5 font-bold text-blue-800 disabled:opacity-60" disabled={pending} onClick={startWorkflow} type="button">Start questionnaire</button> : null}
        {workflow?.state === 'started' ? <button className="mt-4 rounded-full bg-blue-700 px-5 py-2.5 font-bold text-white disabled:opacity-60" disabled={pending} onClick={() => void transition('begin')} type="button">Begin fixed questions</button> : null}
        {workflow?.state === 'collecting' ? (
          <form className="mt-5 grid gap-4 sm:grid-cols-3" onSubmit={submitQuestionnaire}>
            <label className="text-sm font-bold text-slate-800">Concern<select className="auth-input mt-2" name="concern" defaultValue="fever"><option value="fever">Fever</option><option value="digestive">Digestive</option><option value="other">Other</option></select></label>
            <label className="text-sm font-bold text-slate-800">Duration<select className="auth-input mt-2" name="duration" defaultValue="days"><option value="today">Today</option><option value="days">Days</option><option value="weeks">Weeks</option></select></label>
            <label className="text-sm font-bold text-slate-800">Severity<select className="auth-input mt-2" name="severity" defaultValue="mild"><option value="mild">Mild</option><option value="moderate">Moderate</option><option value="severe">Severe</option></select></label>
            <button className="rounded-full bg-blue-700 px-5 py-2.5 font-bold text-white disabled:opacity-60 sm:col-span-3" disabled={pending} type="submit">Review selections</button>
          </form>
        ) : null}
        {workflow?.state === 'review' ? (
          <div className="mt-5 rounded-2xl bg-white p-5">
            <p className="font-bold text-slate-900">Review only — no diagnosis</p>
            <ul className="mt-3 list-disc pl-5 text-sm text-slate-600">{workflow.summary.map((item) => <li key={item}>{item.replace(':', ': ')}</li>)}</ul>
            <button className="mt-4 rounded-full bg-blue-700 px-5 py-2.5 font-bold text-white disabled:opacity-60" disabled={pending} onClick={() => void transition('complete')} type="button">Complete demonstration</button>
          </div>
        ) : null}
        {workflow?.state === 'completed' ? <p className="mt-5 rounded-2xl bg-white p-5 font-bold text-emerald-800" role="status">Questionnaire demonstration complete. No diagnosis or treatment was produced.</p> : null}
      </div>
      {error ? <p className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-800" role="alert">{error}</p> : null}
    </section>
  )
}
