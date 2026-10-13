import { ApiStatus } from '@/components/api-status'

const features = [
  {
    eyebrow: 'Evidence first',
    title: 'Health information assistant',
    description: 'Plain-language answers designed to show their sources and acknowledge uncertainty.',
  },
  {
    eyebrow: 'Your context',
    title: 'Document explanations',
    description: 'A planned private workflow for explaining report terms without inventing diagnoses.',
  },
  {
    eyebrow: 'Safety gates',
    title: 'Structured symptom guidance',
    description: 'Conservative questions with deterministic escalation for possible emergencies.',
  },
] as const

export default function Home() {
  return (
    <div className="min-h-screen overflow-hidden">
      <header className="mx-auto flex w-[min(1180px,calc(100%-2.5rem))] items-center justify-between py-6">
        <a
          className="inline-flex items-center gap-3 font-extrabold outline-none focus-visible:ring-3 focus-visible:ring-amber-400"
          href="#top"
          aria-label="Sehat AI home"
        >
          <span className="grid size-10 place-items-center rounded-[13px] bg-teal-700 text-white shadow-lg shadow-teal-900/15" aria-hidden="true">S</span>
          <span>Sehat AI</span>
        </a>
        <span className="rounded-full border border-emerald-900/15 bg-white/70 px-3 py-2 text-xs font-bold tracking-wider text-slate-600 uppercase max-sm:hidden">
          Foundation preview
        </span>
      </header>

      <main id="top">
        <section className="mx-auto grid w-[min(1180px,calc(100%-2.5rem))] grid-cols-[minmax(0,1.45fr)_minmax(300px,.72fr)] items-center gap-[clamp(2.5rem,7vw,5.75rem)] py-[clamp(4rem,10vw,8.25rem)] max-md:grid-cols-1">
          <div>
            <p className="mb-4 text-xs font-extrabold tracking-[0.13em] text-teal-700 uppercase">Healthcare knowledge, with boundaries</p>
            <h1 className="mb-6 max-w-4xl font-serif text-[clamp(3rem,6.4vw,6.3rem)] leading-[.95] font-medium tracking-[-.055em] text-emerald-950">
              Understand health information with evidence in view.
            </h1>
            <p className="max-w-2xl text-[clamp(1.05rem,1.6vw,1.3rem)] leading-8 text-slate-600">
              Sehat AI is being engineered to help people navigate medical information clearly,
              trace every supported claim, and know when a professional should take over.
            </p>
            <div className="mt-8 flex flex-wrap gap-3 max-sm:flex-col">
              <a className="rounded-full bg-teal-700 px-5 py-3.5 text-center font-bold text-white shadow-lg shadow-teal-900/15 outline-none transition-transform hover:-translate-y-0.5 focus-visible:ring-3 focus-visible:ring-amber-400 motion-reduce:transition-none" href="#capabilities">Explore the plan</a>
              <a className="rounded-full border border-emerald-900/15 bg-white/70 px-5 py-3.5 text-center font-bold outline-none transition-transform hover:-translate-y-0.5 focus-visible:ring-3 focus-visible:ring-amber-400 motion-reduce:transition-none" href="#safety">Read the safety boundary</a>
            </div>
          </div>

          <aside className="rounded-3xl border border-emerald-900/15 bg-white/80 p-7 shadow-2xl shadow-emerald-950/10 backdrop-blur-md" aria-label="Development status">
            <p className="mb-3 text-xs font-extrabold tracking-[0.13em] text-teal-700 uppercase">Milestone 2</p>
            <h2 className="mb-2 text-2xl font-bold text-emerald-950">Local system foundation</h2>
            <p className="mb-5 leading-6 text-slate-600">The interface and typed health API run without database or AI credentials.</p>
            <ApiStatus />
            <dl className="mt-5">
              {[['AI generation', 'Not enabled'], ['Patient data', 'Not collected'], ['Clinical status', 'Not validated']].map(([term, detail]) => (
                <div className="flex justify-between gap-5 border-t border-emerald-900/10 py-3" key={term}>
                  <dt className="text-slate-500">{term}</dt>
                  <dd className="m-0 text-right font-bold text-emerald-950">{detail}</dd>
                </div>
              ))}
            </dl>
          </aside>
        </section>

        <section className="flex items-start gap-5 bg-[#704b30] px-[max(1.5rem,calc((100%-1130px)/2))] py-8 text-amber-50" id="safety" aria-labelledby="safety-title">
          <span className="grid size-9 shrink-0 place-items-center rounded-full border border-amber-300/50 font-black" aria-hidden="true">!</span>
          <div>
            <h2 className="mb-1 font-bold" id="safety-title">This is not medical advice or an emergency service.</h2>
            <p className="m-0 leading-6 text-amber-100/85">Sehat AI will not diagnose, prescribe, or replace qualified care. If someone may be in immediate danger, contact local emergency services now.</p>
          </div>
        </section>

        <section className="mx-auto w-[min(1180px,calc(100%-2.5rem))] py-28" id="capabilities" aria-labelledby="capabilities-title">
          <div className="mb-11 max-w-2xl">
            <p className="mb-4 text-xs font-extrabold tracking-[0.13em] text-teal-700 uppercase">Designed around trust</p>
            <h2 className="font-serif text-[clamp(2.2rem,4vw,4rem)] leading-tight font-medium tracking-[-.045em] text-emerald-950" id="capabilities-title">Useful assistance without pretending certainty</h2>
          </div>
          <div className="grid grid-cols-3 gap-5 max-md:grid-cols-1">
            {features.map((feature, index) => (
              <article className="flex min-h-80 flex-col rounded-3xl border border-emerald-900/15 bg-white/65 p-6" key={feature.title}>
                <span className="mb-14 font-serif text-slate-500">0{index + 1}</span>
                <p className="mb-3 text-xs font-extrabold tracking-[0.13em] text-teal-700 uppercase">{feature.eyebrow}</p>
                <h3 className="mb-3 text-xl font-bold text-emerald-950">{feature.title}</h3>
                <p className="leading-6 text-slate-600">{feature.description}</p>
                <span className="mt-auto self-start rounded-full border border-emerald-900/15 bg-white/70 px-2.5 py-1.5 text-[.65rem] font-bold tracking-wide text-slate-600 uppercase">Planned and test-gated</span>
              </article>
            ))}
          </div>
        </section>
      </main>

      <footer className="mx-auto flex w-[min(1180px,calc(100%-2.5rem))] justify-between gap-5 border-t border-emerald-900/15 py-8 text-sm text-slate-500 max-sm:flex-col">
        <strong className="text-emerald-950">Sehat AI</strong>
        <span>Safety-first engineering in progress</span>
      </footer>
    </div>
  )
}
