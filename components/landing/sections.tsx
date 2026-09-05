import Link from 'next/link'
import { ArrowRight, Layers, ListChecks, Map, MessageSquare, Compass, Wrench } from 'lucide-react'
import { Button } from '@/components/ui/button'

const STEPS = [
  {
    n: '01',
    title: 'Share your profile',
    body: 'Skill level, languages you know, what you are into, and how much time you have.',
  },
  {
    n: '02',
    title: 'Generate ideas',
    body: 'Get four tailored, buildable project ideas — each scored for how well it fits you.',
  },
  {
    n: '03',
    title: 'Get your plan',
    body: 'Pick one and receive a roadmap, feature backlog, tech stack, and an on-call mentor.',
  },
]

const CAPABILITIES = [
  {
    icon: Compass,
    title: 'Ideas that actually fit',
    body: 'Original, specific project concepts calibrated to your skills, interests, and available time — never generic filler.',
  },
  {
    icon: Map,
    title: 'A phased roadmap',
    body: 'A week-by-week plan from walking skeleton to shippable product, with concrete milestones for each phase.',
  },
  {
    icon: ListChecks,
    title: 'A prioritized backlog',
    body: 'Features split into must-have, nice-to-have, and stretch — with effort estimates you can check off as you go.',
  },
  {
    icon: Wrench,
    title: 'A tech stack with reasons',
    body: 'Concrete tool recommendations across frontend, backend, and data — each with a short why that fits your stack.',
  },
  {
    icon: MessageSquare,
    title: 'A mentor on call',
    body: 'Stuck on a decision or an error? Ask your mentor, who already knows the full context of your project.',
  },
  {
    icon: Layers,
    title: 'Everything in one workspace',
    body: 'Your idea, plan, and progress live together and persist in your browser — pick up right where you left off.',
  },
]

export function HowItWorks() {
  return (
    <section className="mx-auto w-full max-w-6xl px-4 py-20 sm:px-6">
      <div className="mb-12 max-w-2xl">
        <p className="font-mono text-xs uppercase tracking-widest text-primary">How it works</p>
        <h2 className="mt-3 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
          From idea to plan in three steps
        </h2>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {STEPS.map((s) => (
          <div key={s.n} className="relative rounded-xl border border-border bg-card p-6">
            <span className="font-mono text-sm text-primary">{s.n}</span>
            <h3 className="mt-3 text-lg font-semibold">{s.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export function Capabilities() {
  return (
    <section className="border-y border-border/60 bg-card/30">
      <div className="mx-auto w-full max-w-6xl px-4 py-20 sm:px-6">
        <div className="mb-12 max-w-2xl">
          <p className="font-mono text-xs uppercase tracking-widest text-primary">What you get</p>
          <h2 className="mt-3 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            A complete plan, not just a prompt
          </h2>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {CAPABILITIES.map((c) => (
            <div key={c.title} className="group rounded-xl border border-border bg-card p-6 transition-colors hover:border-primary/40">
              <div className="grid size-10 place-items-center rounded-lg border border-border bg-background text-primary transition-colors group-hover:border-primary/40">
                <c.icon className="size-5" />
              </div>
              <h3 className="mt-4 font-semibold">{c.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{c.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export function FooterCta() {
  return (
    <section className="relative overflow-hidden">
      <div className="blueprint-grid absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,black,transparent_70%)]" />
      <div className="relative mx-auto flex w-full max-w-6xl flex-col items-center px-4 py-24 text-center sm:px-6">
        <h2 className="max-w-2xl text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
          Your next portfolio project is one profile away
        </h2>
        <p className="mt-4 max-w-xl text-pretty text-muted-foreground">
          Answer a few questions and let ProjectMentor turn your goals into a plan you can start building today.
        </p>
        <Button asChild size="lg" className="mt-8 gap-2">
          <Link href="/onboarding">
            Build my project plan
            <ArrowRight className="size-4" />
          </Link>
        </Button>
      </div>
      <footer className="border-t border-border/60">
        <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-3 px-4 py-6 font-mono text-xs text-muted-foreground sm:flex-row sm:px-6">
          <span>projectmentor — built with the AI SDK on Vercel</span>
          <span>Plans saved locally in your browser</span>
        </div>
      </footer>
    </section>
  )
}
