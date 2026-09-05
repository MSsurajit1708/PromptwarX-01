'use client'

import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

type ChipGroupProps = {
  options: string[]
  selected: string[]
  onChange: (next: string[]) => void
  single?: boolean
}

export function ChipGroup({ options, selected, onChange, single }: ChipGroupProps) {
  function toggle(option: string) {
    if (single) {
      onChange([option])
      return
    }
    onChange(selected.includes(option) ? selected.filter((o) => o !== option) : [...selected, option])
  }

  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => {
        const active = selected.includes(option)
        return (
          <button
            key={option}
            type="button"
            aria-pressed={active}
            onClick={() => toggle(option)}
            className={cn(
              'inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm transition-colors',
              active
                ? 'border-primary bg-primary/15 text-foreground'
                : 'border-border bg-card text-muted-foreground hover:border-primary/40 hover:text-foreground',
            )}
          >
            {active && <Check className="size-3.5 text-primary" />}
            {option}
          </button>
        )
      })}
    </div>
  )
}
