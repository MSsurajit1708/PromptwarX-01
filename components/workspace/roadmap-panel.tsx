import { Circle } from 'lucide-react'
import type { RoadmapPhase } from '@/lib/types'

export function RoadmapPanel({ roadmap }: { roadmap: RoadmapPhase[] }) {
  const total = roadmap.reduce((sum, p) => sum + p.durationWeeks, 0)
  return (
    <div className="space-y-6">
      <p className="font-mono text-xs text-muted-foreground">
        {roadmap.length} phases · ~{total} weeks total
      </p>
      <ol className="relative space-y-6 border-l border-border pl-6">
        {roadmap.map((phase, i) => (
          <li key={i} className="relative">
            <span className="absolute -left-[31px] grid size-6 place-items-center rounded-full border border-primary/40 bg-background font-mono text-[11px] text-primary">
              {i + 1}
            </span>
            <div className="rounded-xl border border-border bg-card p-5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-lg font-semibold">{phase.title}</h3>
                <span className="rounded-full border border-border bg-muted px-2.5 py-0.5 font-mono text-xs text-muted-foreground">
                  {phase.durationWeeks} {phase.durationWeeks === 1 ? 'week' : 'weeks'}
                </span>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{phase.summary}</p>
              <ul className="mt-4 space-y-2">
                {phase.milestones.map((m, mi) => (
                  <li key={mi} className="flex items-start gap-2 text-sm">
                    <Circle className="mt-1 size-3 shrink-0 text-primary" />
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}
