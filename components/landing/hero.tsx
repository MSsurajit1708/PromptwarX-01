import Link from 'next/link'
import { ArrowRight, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-border/60">
      <div className="blueprint-grid pointer-events-none absolute inset-0 [mask-image:radial-gradient(ellipse_at_top,black,transparent_75%)]" />
      <div className="relative mx-auto grid w-full max-w-6xl gap-12 px-4 py-20 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:py-28">
        <div className="flex flex-col items-start justify-center">
          <Badge variant="outline" className="mb-6 gap-1.5 rounded-full border-primary/30 bg-primary/10 py-1 font-mono text-primary">
            <Sparkles className="size-3.5" />
            Your AI project advisor
          </Badge>
          <h1 className="text-balance text-4xl font-semibold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl">
            Stop staring at a blank repo.{' '}
            <span className="text-primary">Ship the right project.</span>
          </h1>
          <p className="mt-6 max-w-xl text-pretty text-lg leading-relaxed text-muted-foreground">
            Tell ProjectMentor your skills and goals. Get tailored project ideas, a week-by-week roadmap,
            a prioritized feature list, a tech stack that fits you, and a mentor to ask along the way.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Button asChild size="lg" className="gap-2">
              <Link href="/onboarding">
                Build my project plan
                <ArrowRight className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href="/generate">Skip to idea generator</Link>
            </Button>
          </div>
          <p className="mt-4 font-mono text-xs text-muted-foreground">
            No account needed — your plan is saved right in your browser.
          </p>
        </div>

        <HeroPreview />
      </div>
    </section>
  )
}

function HeroPreview() {
  return (
    <div className="relative flex items-center justify-center">
      <div className="w-full max-w-md rounded-xl border border-border bg-card/80 p-1 glow-primary">
        <div className="flex items-center gap-1.5 px-3 py-2.5">
          <span className="size-2.5 rounded-full bg-muted-foreground/40" />
          <span className="size-2.5 rounded-full bg-muted-foreground/40" />
          <span className="size-2.5 rounded-full bg-muted-foreground/40" />
          <span className="ml-2 font-mono text-xs text-muted-foreground">projectmentor / new-idea</span>
        </div>
        <div className="space-y-3 rounded-lg bg-background/60 p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="font-mono text-xs text-primary">MATCH 94%</p>
              <h3 className="mt-1 text-lg font-semibold">PR Digest</h3>
              <p className="text-sm text-muted-foreground">An AI teammate that summarizes your repo every morning.</p>
            </div>
            <Badge variant="secondary" className="shrink-0 font-mono text-xs">
              Intermediate
            </Badge>
          </div>
          <div className="grid grid-cols-3 gap-2 font-mono text-xs">
            <div className="rounded-md border border-border bg-card px-2 py-1.5">
              <p className="text-muted-foreground">Est.</p>
              <p className="text-foreground">5 wks</p>
            </div>
            <div className="rounded-md border border-border bg-card px-2 py-1.5">
              <p className="text-muted-foreground">Domain</p>
              <p className="text-foreground">Dev tools</p>
            </div>
            <div className="rounded-md border border-border bg-card px-2 py-1.5">
              <p className="text-muted-foreground">Stack</p>
              <p className="text-foreground">Next.js</p>
            </div>
          </div>
          <div className="space-y-2">
            {[
              { label: 'Foundations', w: '20%' },
              { label: 'Core: webhook ingest', w: '65%' },
              { label: 'Digest + delivery', w: '40%' },
            ].map((r) => (
              <div key={r.label} className="flex items-center gap-3">
                <span className="w-40 shrink-0 truncate font-mono text-xs text-muted-foreground">{r.label}</span>
                <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
                  <span className="block h-full rounded-full bg-primary" style={{ width: r.w }} />
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
