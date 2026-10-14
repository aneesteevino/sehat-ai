'use client'

import { FormEvent, useState } from 'react'

type Evidence = {
  chunk_id: string
  content: string
  citation: {
    source_version_id: string
    title: string
    publisher: string
    canonical_url: string
    locator: string
  }
}
type AnswerResult = {
  status: 'answered' | 'abstained' | 'escalated'
  claims: Array<{ text: string; evidence_ids: string[] }>
  evidence: Evidence[]
  uncertainty: string
  safety_notice: string
  abstention_reason: 'insufficient_evidence' | 'unsafe_input' | null
  escalation: { categories: string[]; message: string; actions: string[] } | null
  usage: {
    provider: string
    model: string
    estimated_cost_usd: number
    attempts: number
  }
}

export function GroundedAnswer() {
  const [result, setResult] = useState<AnswerResult | null>(null)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  async function ask(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const question = new FormData(event.currentTarget).get('question')?.toString().trim() ?? ''
    if (question.length < 2) return

    setPending(true)
    setError('')
    setResult(null)
    try {
      const response = await fetch('/api/answers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const payload = await response.json() as AnswerResult | { error?: string }
      if (!response.ok) {
        setError('error' in payload && payload.error ? payload.error : 'Unable to prepare an answer.')
        return
      }
      setResult(payload as AnswerResult)
    } catch {
      setError('Unable to reach grounded answers. Please try again.')
    } finally {
      setPending(false)
    }
  }

  return (
    <section className="mt-12 rounded-3xl border border-emerald-900/15 bg-emerald-950 p-6 text-white sm:p-8" aria-labelledby="grounded-answer-title">
      <p className="text-xs font-extrabold tracking-[.13em] text-teal-200 uppercase">Milestone 5 evaluation preview</p>
      <h2 className="mt-3 font-serif text-3xl font-medium tracking-[-.03em]" id="grounded-answer-title">Ask the approved evidence</h2>
      <p className="mt-3 max-w-2xl leading-7 text-emerald-50/75">A deterministic mock composes a preview only after retrieval. It abstains when the small evaluation corpus is not a reliable match.</p>
      <form className="mt-6 flex flex-col gap-3 sm:flex-row" onSubmit={ask}>
        <label className="sr-only" htmlFor="answer-question">Question for grounded answer</label>
        <input className="auth-input flex-1 bg-white text-slate-900" id="answer-question" name="question" minLength={2} maxLength={500} placeholder="For example: How long should hands be scrubbed with soap?" required />
        <button className="rounded-full bg-amber-300 px-6 py-3 font-bold text-emerald-950 outline-none hover:bg-amber-200 focus-visible:ring-3 focus-visible:ring-white disabled:cursor-wait disabled:opacity-60" disabled={pending} type="submit">
          {pending ? 'Checking evidence…' : 'Prepare grounded answer'}
        </button>
      </form>

      {error ? <p className="mt-5 rounded-xl border border-red-200/30 bg-red-950/50 p-3 text-sm text-red-100" role="alert" aria-live="polite">{error}</p> : null}
      {result ? (
        <div className="mt-8 space-y-6" aria-live="polite">
          <section aria-labelledby="answer-result-title">
            <p className="text-xs font-bold tracking-wider text-teal-200 uppercase">Answer</p>
            <h3 className="mt-2 text-xl font-bold" id="answer-result-title">
              {result.status === 'answered'
                ? 'Evidence-grounded preview'
                : result.status === 'escalated' ? 'Get emergency help now' : 'Not enough approved evidence'}
            </h3>
            {result.status === 'answered' ? (
              <ol className="mt-4 space-y-3">
                {result.claims.map((claim, claimIndex) => (
                  <li className="leading-7 text-emerald-50" key={`${claim.text}-${claimIndex}`}>
                    {claim.text}{' '}
                    {claim.evidence_ids.map((evidenceId) => {
                      const evidenceIndex = result.evidence.findIndex((item) => item.chunk_id === evidenceId)
                      return <a className="ml-1 font-bold text-amber-300 underline underline-offset-4" href={`#answer-evidence-${evidenceId}`} key={evidenceId} aria-label={`View evidence ${evidenceIndex + 1}`}>[{evidenceIndex + 1}]</a>
                    })}
                  </li>
                ))}
              </ol>
            ) : result.status === 'escalated' && result.escalation ? (
              <div className="mt-4 rounded-2xl border border-red-300/40 bg-red-950/60 p-5" role="alert">
                <p className="font-bold text-red-100">{result.escalation.message}</p>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-red-100/90">
                  {result.escalation.actions.map((action) => <li key={action}>{action}</li>)}
                </ul>
              </div>
            ) : <p className="mt-3 leading-7 text-emerald-50">I can’t answer this reliably from the currently approved sources.</p>}
          </section>

          {result.evidence.length ? (
            <section aria-labelledby="answer-evidence-title">
              <h3 className="text-xs font-bold tracking-wider text-teal-200 uppercase" id="answer-evidence-title">Evidence</h3>
              <ol className="mt-3 space-y-3">
                {result.evidence.map((item, index) => (
                  <li className="rounded-2xl bg-white/8 p-4" id={`answer-evidence-${item.chunk_id}`} key={item.chunk_id}>
                    <p className="leading-7 text-emerald-50"><span className="font-bold text-amber-300">[{index + 1}]</span> {item.content}</p>
                    <p className="mt-3 text-sm text-emerald-100/70">
                      <a className="font-bold text-teal-200 underline underline-offset-4" href={item.citation.canonical_url} rel="noreferrer" target="_blank">{item.citation.title}</a>
                      {' · '}{item.citation.publisher}{' · '}{item.citation.locator}
                    </p>
                  </li>
                ))}
              </ol>
            </section>
          ) : null}

          <section className="grid gap-3 sm:grid-cols-2" aria-label="Answer limitations">
            <div className="rounded-2xl border border-teal-200/20 p-4">
              <h3 className="font-bold text-teal-200">Uncertainty</h3>
              <p className="mt-2 text-sm leading-6 text-emerald-50/80">{result.uncertainty}</p>
            </div>
            <div className="rounded-2xl border border-amber-200/20 p-4">
              <h3 className="font-bold text-amber-300">Safety limitations</h3>
              <p className="mt-2 text-sm leading-6 text-emerald-50/80">{result.safety_notice}</p>
            </div>
          </section>
          <p className="text-xs text-emerald-100/60">Provider: {result.usage.provider} / {result.usage.model} · attempts: {result.usage.attempts} · estimated cost: ${result.usage.estimated_cost_usd.toFixed(6)}</p>
        </div>
      ) : null}
    </section>
  )
}

