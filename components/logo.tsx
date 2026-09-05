import { cn } from '@/lib/utils'

export function Logo({ className }: { className?: string }) {
  return (
    <span className={cn('flex items-center gap-2 font-mono text-sm font-semibold tracking-tight', className)}>
      <span
        aria-hidden
        className="grid size-6 place-items-center rounded-[5px] bg-primary text-primary-foreground"
      >
        <svg viewBox="0 0 24 24" className="size-4" fill="none" stroke="currentColor" strokeWidth={2.2}>
          <path d="M4 18 L10 6 L14 15 L20 5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </span>
      <span className="text-foreground">
        project<span className="text-primary">mentor</span>
      </span>
    </span>
  )
}
