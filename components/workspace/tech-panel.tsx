import { Layout, Server, Database, Wrench } from 'lucide-react'
import type { TechChoice, TechStack } from '@/lib/types'

const GROUPS: { key: keyof TechStack; label: string; icon: typeof Layout }[] = [
  { key: 'frontend', label: 'Frontend', icon: Layout },
  { key: 'backend', label: 'Backend', icon: Server },
  { key: 'data', label: 'Data', icon: Database },
  { key: 'tooling', label: 'Tooling', icon: Wrench },
]

export function TechPanel({ stack }: { stack: TechStack }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {GROUPS.map(({ key, label, icon: Icon }) => {
        const items = stack[key] as TechChoice[]
        if (!items?.length) return null
        return (
          <div key={key} className="rounded-xl border border-border bg-card p-5">
            <div className="flex items-center gap-2">
              <div className="grid size-8 place-items-center rounded-lg border border-border bg-background text-primary">
                <Icon className="size-4" />
              </div>
              <h3 className="font-mono text-xs uppercase tracking-widest text-muted-foreground">{label}</h3>
            </div>
            <ul className="mt-4 space-y-4">
              {items.map((item) => (
                <li key={item.name}>
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="font-medium">{item.name}</span>
                    <span className="font-mono text-[11px] text-muted-foreground">{item.category}</span>
                  </div>
                  <p className="mt-1 text-sm leading-relaxed text-muted-foreground">{item.reason}</p>
                </li>
              ))}
            </ul>
          </div>
        )
      })}
    </div>
  )
}
