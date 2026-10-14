import { redirect } from 'next/navigation'

import { SignOutButton } from '@/components/sign-out-button'
import { currentUser } from '@/lib/auth'

const roleLabels = { patient: 'Patient', clinician: 'Clinician', admin: 'Administrator' } as const

export default async function WorkspacePage() {
  const user = await currentUser()
  if (!user) redirect('/sign-in')

  return (
    <main className="mx-auto min-h-screen w-[min(1000px,calc(100%-2.5rem))] py-8">
      <header className="flex items-center justify-between gap-4 border-b border-emerald-900/15 pb-6">
        <div>
          <p className="text-xs font-extrabold tracking-[.13em] text-teal-700 uppercase">Sehat AI workspace</p>
          <p className="mt-1 text-sm text-slate-500">Authenticated local preview</p>
        </div>
        <SignOutButton />
      </header>
      <section className="py-16" aria-labelledby="workspace-title">
        <span className="rounded-full border border-teal-900/15 bg-teal-50 px-3 py-2 text-xs font-bold tracking-wide text-teal-800 uppercase">{roleLabels[user.role]} access</span>
        <h1 className="mt-6 font-serif text-[clamp(2.6rem,6vw,5rem)] leading-none font-medium tracking-[-.05em] text-emerald-950" id="workspace-title">Hello, {user.display_name}</h1>
        <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">Your identity and session are active. Health features remain disabled until their safety and evidence gates are implemented.</p>
        <div className="mt-10 grid gap-5 sm:grid-cols-2">
          <article className="rounded-3xl border border-emerald-900/15 bg-white/75 p-6">
            <h2 className="font-bold text-emerald-950">Account boundary</h2>
            <p className="mt-2 break-all text-sm text-slate-600">{user.email}</p>
            <p className="mt-4 text-sm leading-6 text-slate-500">Role checks are enforced by the API, not trusted from browser state.</p>
          </article>
          <article className="rounded-3xl border border-amber-900/15 bg-amber-50/70 p-6">
            <h2 className="font-bold text-amber-950">Safety boundary</h2>
            <p className="mt-2 text-sm leading-6 text-amber-900/75">No diagnosis, prescribing, clinical interpretation, or emergency response is enabled.</p>
          </article>
        </div>
      </section>
    </main>
  )
}
