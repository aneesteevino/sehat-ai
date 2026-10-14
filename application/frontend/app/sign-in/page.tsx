import Link from 'next/link'

import { AuthForm } from '@/components/auth-form'

export default function SignInPage() {
  return (
    <main className="grid min-h-screen place-items-center px-5 py-14">
      <section className="w-full max-w-md rounded-3xl border border-emerald-900/15 bg-white/85 p-8 shadow-2xl shadow-emerald-950/10" aria-labelledby="sign-in-title">
        <Link className="text-sm font-bold text-teal-700 hover:text-teal-900" href="/">← Sehat AI</Link>
        <p className="mt-8 text-xs font-extrabold tracking-[.13em] text-teal-700 uppercase">Private workspace</p>
        <h1 className="mt-3 font-serif text-4xl font-medium tracking-[-.04em] text-emerald-950" id="sign-in-title">Welcome back</h1>
        <p className="mt-3 leading-6 text-slate-600">Sign in to continue. Sehat AI is not an emergency service.</p>
        <AuthForm mode="login" />
        <p className="mt-6 text-center text-sm text-slate-600">New here? <Link className="font-bold text-teal-700" href="/sign-up">Create an account</Link></p>
      </section>
    </main>
  )
}
