'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { RefreshCw, Sparkles, Wand2, AlertTriangle, FolderOpen, Pencil } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { IdeaCard } from '@/components/idea-card'
import { useStore } from '@/lib/store'
import { FALLBACK_IDEAS, fallbackPlan } from '@/lib/data'
import { difficultyClasses } from '@/lib/ui'
import { cn } from '@/lib/utils'
import type { Idea, ProjectPlan } from '@/lib/types'

export function GenerateClient() {
  const router = useRouter()
  const { profile, projects, hydrated, createProject, setPlanStatus, setProjectPlan } = useStore()

  const [ideas, setIdeas] = useState<Idea[]>([])
  const [status, setStatus] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [usedFallback, setUsedFallback] = useState(false)
  const [prompt, setPrompt] = useState('')
  const [selecting, setSelecting] = useState<string | null>(null)

  useEffect(() => {
    if (hydrated && !profile) router.replace('/onboarding')
  }, [hydrated, profile, router])

  async function generate() {
    if (!profile) return
    setStatus('loading')
    setUsedFallback(false)
    try {
      const res = await fetch('/api/ideas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile, prompt: prompt.trim() || undefined }),
      })
      if (!res.ok) throw new Error('request failed')
      const data = (await res.json()) as { ideas: Omit<Idea, 'id'>[] }
      setIdeas(data.ideas.map((idea, i) => ({ ...idea, id: `idea_${Date.now()}_${i}` })))
      setStatus('ready')
    } catch {
      setIdeas(FALLBACK_IDEAS.map((i) => ({ ...i, id: `${i.id}_${Date.now()}` })))
      setUsedFallback(true)
      setStatus('ready')
    }
  }

  // Auto-generate the first batch once a profile is present.
  useEffect(() => {
    if (hydrated && profile && status === 'idle') generate()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hydrated, profile])

  async function selectIdea(idea: Idea) {
    if (!profile) return
    setSelecting(idea.id)
    const project = createProject(idea)
    setPlanStatus(project.id, 'loading')
    router.push(`/project/${project.id}`)
    try {
      const res = await fetch('/api/project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea, profile }),
      })
      if (!res.ok) throw new Error('request failed')
      const raw = (await res.json()) as Omit<ProjectPlan, 'features'> & {
        features: Omit<ProjectPlan['features'][number], 'id' | 'done'>[]
      }
      const plan: ProjectPlan = {
        ...raw,
        features: raw.features.map((f, i) => ({ ...f, id: `feat_${i}`, done: false })),
      }
      setProjectPlan(project.id, plan)
    } catch {
      setProjectPlan(project.id, fallbackPlan(idea))
    }
  }

  if (!hydrated || !profile) {
    return (
      <div className="grid gap-4 md:grid-cols-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-72 w-full rounded-xl" />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-10">
      <ProfileSummary />

      {projects.length > 0 && <ExistingProjects />}

      <section className="space-y-4">
        <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-4 sm:flex-row sm:items-center">
          <div className="flex flex-1 items-center gap-2">
            <Wand2 className="size-4 shrink-0 text-primary" />
            <Input
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.nativeEvent.isComposing && e.keyCode !== 229) {
                  e.preventDefault()
                  generate()
                }
              }}
              placeholder="Optional: nudge the ideas (e.g. 'something with maps' or 'a CLI tool')"
              className="border-0 bg-transparent px-0 shadow-none focus-visible:ring-0"
            />
          </div>
          <Button onClick={generate} disabled={status === 'loading'} className="gap-2">
            {status === 'loading' ? (
              <RefreshCw className="size-4 animate-spin" />
            ) : (
              <Sparkles className="size-4" />
            )}
            {ideas.length ? 'Regenerate' : 'Generate ideas'}
          </Button>
        </div>

        {usedFallback && status === 'ready' && (
          <div className="flex items-center gap-2 rounded-lg border border-chart-3/40 bg-chart-3/10 px-3 py-2 text-sm text-chart-3">
            <AlertTriangle className="size-4" />
            Live AI is unavailable right now, so these are sample ideas. Try regenerating in a moment.
          </div>
        )}

        {status === 'loading' ? (
          <div className="grid gap-4 md:grid-cols-2">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-72 w-full rounded-xl" />
            ))}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {ideas.map((idea) => (
              <IdeaCard key={idea.id} idea={idea} onSelect={selectIdea} busy={selecting === idea.id} />
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

function ProfileSummary() {
  const { profile } = useStore()
  if (!profile) return null
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-xl border border-border bg-card/50 px-4 py-3 text-sm">
      <span className="font-mono text-xs uppercase tracking-wider text-muted-foreground">Profile</span>
      <Badge variant="secondary" className="font-mono text-xs capitalize">
        {profile.skillLevel}
      </Badge>
      <span className="text-muted-foreground">{profile.languages.slice(0, 4).join(', ')}</span>
      <span className="text-muted-foreground">·</span>
      <span className="text-muted-foreground">{profile.interests.slice(0, 3).join(', ')}</span>
      <Button asChild variant="ghost" size="sm" className="ml-auto gap-1.5">
        <Link href="/onboarding">
          <Pencil className="size-3.5" />
          Edit
        </Link>
      </Button>
    </div>
  )
}

function ExistingProjects() {
  const { projects } = useStore()
  return (
    <section className="space-y-3">
      <h2 className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-muted-foreground">
        <FolderOpen className="size-4" />
        Your projects
      </h2>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {projects.map((p) => (
          <Link
            key={p.id}
            href={`/project/${p.id}`}
            className="group rounded-xl border border-border bg-card p-4 transition-colors hover:border-primary/40"
          >
            <div className="flex items-center justify-between">
              <span className={cn('rounded-full border px-2 py-0.5 font-mono text-[11px]', difficultyClasses(p.idea.difficulty))}>
                {p.idea.difficulty}
              </span>
              <span className="font-mono text-[11px] text-muted-foreground">
                {p.planStatus === 'loading' ? 'planning…' : 'ready'}
              </span>
            </div>
            <p className="mt-3 font-semibold group-hover:text-primary">{p.idea.title}</p>
            <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">{p.idea.tagline}</p>
          </Link>
        ))}
      </div>
    </section>
  )
}
