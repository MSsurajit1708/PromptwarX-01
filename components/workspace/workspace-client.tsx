'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Clock, Layers, RefreshCw, Trash2, AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { RoadmapPanel } from '@/components/workspace/roadmap-panel'
import { FeaturesPanel } from '@/components/workspace/features-panel'
import { TechPanel } from '@/components/workspace/tech-panel'
import { MentorChat } from '@/components/workspace/mentor-chat'
import { useStore } from '@/lib/store'
import { fallbackPlan } from '@/lib/data'
import { difficultyClasses } from '@/lib/ui'
import { cn } from '@/lib/utils'
import type { ProjectPlan } from '@/lib/types'

export function WorkspaceClient({ projectId }: { projectId: string }) {
  const router = useRouter()
  const { hydrated, getProject, profile, setPlanStatus, setProjectPlan, toggleFeature, deleteProject } = useStore()
  const project = getProject(projectId)

  const [regenerating, setRegenerating] = useState(false)

  async function buildPlan() {
    if (!project) return
    setPlanStatus(project.id, 'loading')
    try {
      const res = await fetch('/api/project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea: project.idea, profile }),
      })
      if (!res.ok) throw new Error('failed')
      const raw = (await res.json()) as Omit<ProjectPlan, 'features'> & {
        features: Omit<ProjectPlan['features'][number], 'id' | 'done'>[]
      }
      const plan: ProjectPlan = {
        ...raw,
        features: raw.features.map((f, i) => ({ ...f, id: `feat_${i}`, done: false })),
      }
      setProjectPlan(project.id, plan)
    } catch {
      setProjectPlan(project.id, fallbackPlan(project.idea))
    } finally {
      setRegenerating(false)
    }
  }

  // If we land on a project whose plan generation was interrupted, kick it off.
  useEffect(() => {
    if (project && project.planStatus === 'loading' && !project.plan) buildPlan()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [project?.id, project?.planStatus])

  if (!hydrated) {
    return <Skeleton className="h-96 w-full rounded-xl" />
  }

  if (!project) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-border bg-card py-20 text-center">
        <AlertTriangle className="size-8 text-muted-foreground" />
        <h2 className="mt-4 text-xl font-semibold">Project not found</h2>
        <p className="mt-2 max-w-sm text-sm text-muted-foreground">
          This project may have been deleted, or you opened it in a different browser.
        </p>
        <Button asChild className="mt-6">
          <Link href="/generate">Back to ideas</Link>
        </Button>
      </div>
    )
  }

  const { idea, plan, planStatus } = project
  const planLoading = planStatus === 'loading' || (!plan && planStatus !== 'error')

  function handleDelete() {
    deleteProject(project!.id)
    router.push('/generate')
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <Button asChild variant="ghost" size="sm" className="gap-1.5 text-muted-foreground">
          <Link href="/generate">
            <ArrowLeft className="size-4" />
            All ideas
          </Link>
        </Button>
        <Button variant="ghost" size="sm" onClick={handleDelete} className="gap-1.5 text-muted-foreground hover:text-destructive">
          <Trash2 className="size-4" />
          Delete
        </Button>
      </div>

      <header className="rounded-2xl border border-border bg-card p-6 sm:p-8">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="outline" className={cn('font-mono text-xs', difficultyClasses(idea.difficulty))}>
            {idea.difficulty}
          </Badge>
          <span className="font-mono text-xs text-muted-foreground">{idea.domain}</span>
        </div>
        <h1 className="mt-4 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">{idea.title}</h1>
        <p className="mt-2 text-lg text-primary">{idea.tagline}</p>
        <p className="mt-4 max-w-2xl text-pretty leading-relaxed text-muted-foreground">{idea.description}</p>
        <div className="mt-5 flex flex-wrap items-center gap-4 font-mono text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1.5">
            <Clock className="size-3.5" />
            {idea.estimatedWeeks} weeks
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Layers className="size-3.5" />
            {idea.coreConcepts.join(' · ')}
          </span>
        </div>
      </header>

      <Tabs defaultValue="roadmap" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="roadmap">Roadmap</TabsTrigger>
          <TabsTrigger value="features">Features</TabsTrigger>
          <TabsTrigger value="stack">Tech stack</TabsTrigger>
          <TabsTrigger value="mentor">Mentor</TabsTrigger>
        </TabsList>

        <div className="mt-6">
          <TabsContent value="roadmap">
            {planLoading ? (
              <PlanSkeleton label="Charting your roadmap…" />
            ) : plan ? (
              <RoadmapPanel roadmap={plan.roadmap} />
            ) : (
              <PlanError onRetry={buildPlan} regenerating={regenerating} setRegenerating={setRegenerating} />
            )}
          </TabsContent>

          <TabsContent value="features">
            {planLoading ? (
              <PlanSkeleton label="Prioritizing features…" />
            ) : plan ? (
              <FeaturesPanel features={plan.features} onToggle={(fid) => toggleFeature(project.id, fid)} />
            ) : (
              <PlanError onRetry={buildPlan} regenerating={regenerating} setRegenerating={setRegenerating} />
            )}
          </TabsContent>

          <TabsContent value="stack">
            {planLoading ? (
              <PlanSkeleton label="Choosing a tech stack…" />
            ) : plan ? (
              <TechPanel stack={plan.techStack} />
            ) : (
              <PlanError onRetry={buildPlan} regenerating={regenerating} setRegenerating={setRegenerating} />
            )}
          </TabsContent>

          <TabsContent value="mentor">
            <MentorChat project={project} />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  )
}

function PlanSkeleton({ label }: { label: string }) {
  return (
    <div className="space-y-4">
      <p className="flex items-center gap-2 font-mono text-xs text-primary">
        <RefreshCw className="size-3.5 animate-spin" />
        {label}
      </p>
      {Array.from({ length: 3 }).map((_, i) => (
        <Skeleton key={i} className="h-28 w-full rounded-xl" />
      ))}
    </div>
  )
}

function PlanError({
  onRetry,
  regenerating,
  setRegenerating,
}: {
  onRetry: () => void
  regenerating: boolean
  setRegenerating: (v: boolean) => void
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-border bg-card py-16 text-center">
      <AlertTriangle className="size-7 text-muted-foreground" />
      <p className="mt-3 text-sm text-muted-foreground">We couldn&apos;t build this plan. Try again.</p>
      <Button
        className="mt-5 gap-2"
        disabled={regenerating}
        onClick={() => {
          setRegenerating(true)
          onRetry()
        }}
      >
        <RefreshCw className={cn('size-4', regenerating && 'animate-spin')} />
        Retry
      </Button>
    </div>
  )
}
