'use client'

import { FormEvent, useState } from 'react'

type Evidence = {
  chunk_id: string
  content: string
  score: number
  content_trust: 'untrusted'
  citation: {
    source_id: string
    source_version_id: string
    title: string
    publisher: string
    canonical_url: string
    locator: string
  }
}

type SearchResult = {
  query: string
  evidence: Evidence[]
  generated_answer: null
  disclaimer: string
}

export function EvidenceSearch() {
  const [result, setResult] = useState<SearchResult | null>(null)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const query = new FormData(event.currentTarget).get('query')?.toString().trim() ?? ''
    if (query.length < 2) return

    setPending(true)
    setError('')
    setResult(null)
    try {
      const response = await fetch('/api/knowledge/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit: 5 }),
      })
      const payload = await response.json() as SearchResult | { error?: string }
      if (!response.ok) {
        setError('error' in payload && payload.error ? payload.error : 'Unable to search evidence.')
        return
      }
      setResult(payload as SearchResult)
    } catch {
      setError('Unable to reach evidence search. Please try again.')
    } finally {
      setPending(false)
    }
  }

  return (
    <section className="mt-12 rounded-3xl border border-emerald-900/15 bg-white/80 p-6 sm:p-8" aria-labelledby="evidence-search-title">
      <p className="text-xs font-extrabold tracking-[.13em] text-teal-700 uppercase">Milestone 4 preview</p>
      <h2 className="mt-3 font-serif text-3xl font-medium tracking-[-.03em] text-emerald-950" id="evidence-search-title">Search approved evidence</h2>
      <p className="mt-3 max-w-2xl leading-7 text-slate-600">This searches two versioned evaluation summaries and returns source excerpts only. It does not generate medical advice.</p>
      <form className="mt-6 flex flex-col gap-3 sm:flex-row" onSubmit={search} role="search">
        <label className="sr-only" htmlFor="evidence-query">Evidence question</label>
        <input className="auth-input flex-1" id="evidence-query" name="query" minLength={2} maxLength={500} placeholder="For example: How long should hands be scrubbed?" required />
        <button className="rounded-full bg-teal-700 px-6 py-3 font-bold text-white outline-none hover:bg-teal-800 focus-visible:ring-3 focus-visible:ring-amber-400 disabled:cursor-wait disabled:opacity-60" disabled={pending} type="submit">
          {pending ? 'Searching…' : 'Search evidence'}
        </button>
      </form>

      {error ? <p className="mt-5 rounded-xl border border-red-900/20 bg-red-50 p-3 text-sm text-red-800" role="alert" aria-live="polite">{error}</p> : null}
      {result ? (
        <div className="mt-7" aria-live="polite">
          <p className="text-sm font-bold text-emerald-950">{result.evidence.length} evidence {result.evidence.length === 1 ? 'match' : 'matches'}</p>
          {result.evidence.length ? (
            <ol className="mt-4 space-y-4">
              {result.evidence.map((item) => (
                <li className="rounded-2xl border border-emerald-900/10 bg-emerald-50/45 p-5" key={item.chunk_id}>
                  <p className="leading-7 text-slate-700">{item.content}</p>
                  <p className="mt-4 text-sm text-slate-500">
                    <a className="font-bold text-teal-700 underline decoration-teal-700/30 underline-offset-4 hover:text-teal-900" href={item.citation.canonical_url} rel="noreferrer" target="_blank">{item.citation.title}</a>
                    {' · '}{item.citation.publisher}{' · '}{item.citation.locator}
                  </p>
                </li>
              ))}
            </ol>
          ) : <p className="mt-4 text-sm text-slate-600">No approved evidence matched this query.</p>}
          <p className="mt-5 text-sm font-medium text-amber-900">{result.disclaimer}</p>
        </div>
      ) : null}
    </section>
  )
}
