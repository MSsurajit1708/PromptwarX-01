'use client'

import { ArrowRight, Clock, Layers } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { difficultyClasses } from '@/lib/ui'
import { cn } from '@/lib/utils'
import type { Idea } from '@/lib/types'

export function IdeaCard({ idea, onSelect, busy }: { idea: Idea; onSelect: (idea: Idea) => void; busy?: boolean }) {
  return (
    <article className="group flex flex-col rounded-xl border border-border bg-card p-6 transition-colors hover:border-primary/40">
      <div className="flex items-start justify-between gap-3">
        <Badge variant="outline" className={cn('font-mono text-xs', difficultyClasses(idea.difficulty))}>
          {idea.difficulty}
        </Badge>
        <span className="font-mono text-xs text-muted-foreground">{idea.domain}</span>
      </div>

      <h3 className="mt-4 text-xl font-semibold tracking-tight">{idea.title}</h3>
      <p className="mt-1 text-sm text-primary">{idea.tagline}</p>
      <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{idea.description}</p>

      <div className="mt-4 rounded-lg border border-border bg-background/50 p-3">
        <p className="font-mono text-[11px] uppercase tracking-wider text-muted-foreground">Why it fits you</p>
        <p className="mt-1 text-sm text-foreground">{idea.whyMatch}</p>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 font-mono text-xs text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <Clock className="size-3.5" />
          {idea.estimatedWeeks} weeks
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Layers className="size-3.5" />
          {idea.coreConcepts.join(' · ')}
        </span>
      </div>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {idea.tags.map((t) => (
          <Badge key={t} variant="secondary" className="font-mono text-[11px]">
            {t}
          </Badge>
        ))}
      </div>

      <Button onClick={() => onSelect(idea)} disabled={busy} className="mt-6 w-full gap-2">
        {busy ? 'Building plan...' : 'Start this project'}
        {!busy && <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" />}
      </Button>
    </article>
  )
}
