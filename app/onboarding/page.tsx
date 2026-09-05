import { SiteHeader } from '@/components/site-header'
import { OnboardingForm } from '@/components/onboarding-form'

export default function OnboardingPage() {
  return (
    <main className="min-h-dvh">
      <SiteHeader />
      <div className="mx-auto w-full max-w-3xl px-4 py-12 sm:px-6 lg:py-16">
        <header className="mb-10">
          <p className="font-mono text-xs uppercase tracking-widest text-primary">Your profile</p>
          <h1 className="mt-3 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Tell your mentor about you
          </h1>
          <p className="mt-3 max-w-xl text-pretty text-muted-foreground">
            The more honest you are, the better your project ideas and plan will fit. This stays in your browser.
          </p>
        </header>
        <OnboardingForm />
      </div>
    </main>
  )
}
