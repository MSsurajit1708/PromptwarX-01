'use client'

import { Checkbox } from '@/components/ui/checkbox'
import { Progress } from '@/components/ui/progress'
import { priorityClasses } from '@/lib/ui'
import { cn } from '@/lib/utils'
import type { Feature } from '@/lib/types'

const EFFORT_LABEL: Record<Feature['effort'], string> = { S: 'Small', M: 'Medium', L: 'Large' }

export function FeaturesPanel({
  features,
  onToggle,
}: {
  features: Feature[]
  onToggle: (featureId: string) => void
}) {
  const done = features.filter((f) => f.done).length
  const pct = features.length ? Math.round((done / features.length) * 100) : 0

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-4">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium">Build progress</span>
          <span className="font-mono text-muted-foreground">
            {done}/{features.length} done
          </span>
        </div>
        <Progress value={pct} className="mt-3" />
      </div>

      <ul className="space-y-2">
        {features.map((f) => (
          <li
            key={f.id}
            className={cn(
              'flex items-start gap-3 rounded-xl border border-border bg-card p-4 transition-colors',
              f.done && 'opacity-60',
            )}
          >
            <Checkbox
              id={f.id}
              checked={f.done}
              onCheckedChange={() => onToggle(f.id)}
              className="mt-0.5"
            />
            <div className="min-w-0 flex-1">
              <label htmlFor={f.id} className="flex cursor-pointer flex-wrap items-center gap-2">
                <span className={cn('font-medium', f.done && 'line-through')}>{f.title}</span>
                <span className={cn('rounded-full border px-2 py-0.5 font-mono text-[11px]', priorityClasses(f.priority))}>
                  {f.priority}
                </span>
                <span className="rounded-full border border-border bg-muted px-2 py-0.5 font-mono text-[11px] text-muted-foreground">
                  {EFFORT_LABEL[f.effort]}
                </span>
              </label>
              <p className="mt-1 text-sm text-muted-foreground">{f.description}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
