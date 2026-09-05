import { SiteHeader } from '@/components/site-header'
import { GenerateClient } from '@/components/generate-client'

export default function GeneratePage() {
  return (
    <main className="min-h-dvh">
      <SiteHeader />
      <div className="mx-auto w-full max-w-5xl px-4 py-12 sm:px-6">
        <header className="mb-8">
          <p className="font-mono text-xs uppercase tracking-widest text-primary">Idea generator</p>
          <h1 className="mt-3 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Project ideas, tailored to you
          </h1>
          <p className="mt-3 max-w-xl text-pretty text-muted-foreground">
            Pick the one that excites you and your mentor will build out a full plan.
          </p>
        </header>
        <GenerateClient />
      </div>
    </main>
  )
}
